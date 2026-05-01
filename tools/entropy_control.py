from __future__ import annotations

import argparse
import json
import py_compile
import re
import shutil
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOC_ROOTS = [ROOT, ROOT / "docs", ROOT / "runtime" / "tasks"]
TASK_ROOT = ROOT / "runtime" / "tasks"
QUEUE_DIR = TASK_ROOT / "queue"
MAINTENANCE_DIR = ROOT / "artifacts" / "maintenance"
QUALITY_SCORE_PATH = ROOT / "docs" / "QUALITY_SCORE.md"

SEVERITY_ORDER = {"info": 0, "low": 1, "medium": 2, "high": 3}
SEVERITY_WEIGHTS = {"info": 0, "low": 3, "medium": 10, "high": 25}
COMMON_HEADINGS = {
    "acceptance criteria",
    "completed work",
    "goal",
    "open decisions",
    "optional fields",
    "output contract",
    "planned",
    "required fields",
    "responsibilities",
    "scope",
    "status",
    "verification",
}
TOP_LEVEL_PATHS = {
    "AGENTS.md",
    "ARCHITECTURE.md",
    "PLANS.md",
    "README.md",
    "artifacts",
    "docs",
    "evals",
    "references",
    "runtime",
    "tools",
}


@dataclass
class Finding:
    id: str
    severity: str
    dimension: str
    category: str
    title: str
    detail: str
    paths: list[str]
    control: str
    recommendation: str


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def relative(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def stable_id(prefix: str, value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    slug = slug[:70].strip("-") or "finding"
    return f"{prefix}-{slug}"


def markdown_files() -> list[Path]:
    paths: set[Path] = set()
    for root in DOC_ROOTS:
        if root == ROOT:
            paths.update(path for path in root.glob("*.md") if path.is_file())
        elif root.exists():
            paths.update(path for path in root.rglob("*.md") if path.is_file())
    return sorted(paths)


def add_finding(
    findings: list[Finding],
    *,
    severity: str,
    dimension: str,
    category: str,
    title: str,
    detail: str,
    paths: list[Path | str],
    control: str,
    recommendation: str,
) -> None:
    normalized_paths = [relative(path) if isinstance(path, Path) else path for path in paths]
    findings.append(
        Finding(
            id=stable_id(category, title + " " + " ".join(normalized_paths)),
            severity=severity,
            dimension=dimension,
            category=category,
            title=title,
            detail=detail,
            paths=normalized_paths,
            control=control,
            recommendation=recommendation,
        )
    )


def collect_structure_findings(findings: list[Finding]) -> None:
    tools_dir = ROOT / "tools"
    sys.path.insert(0, str(tools_dir))
    try:
        from validate_harness_structure import REQUIRED_PATHS, collect_guardrail_failures
    except Exception as exc:  # noqa: BLE001 - report import failures as harness code health.
        add_finding(
            findings,
            severity="high",
            dimension="guardrails",
            category="structure",
            title="Could not import structural validator",
            detail=str(exc),
            paths=["tools/validate_harness_structure.py"],
            control="Python import",
            recommendation="Repair the structural validator so entropy control can reuse it.",
        )
        return

    missing = [relative(ROOT / item) for item in REQUIRED_PATHS if not (ROOT / item).exists()]
    if missing:
        add_finding(
            findings,
            severity="high",
            dimension="guardrails",
            category="structure",
            title="Required harness paths are missing",
            detail=", ".join(missing),
            paths=missing,
            control="Required path inventory",
            recommendation="Restore the required files or update the structural contract intentionally.",
        )

    guardrail_failures = collect_guardrail_failures()
    if guardrail_failures:
        add_finding(
            findings,
            severity="high",
            dimension="guardrails",
            category="structure",
            title="Task guardrail validation failed",
            detail=" | ".join(guardrail_failures),
            paths=["runtime/tasks"],
            control="Task schema and state validation",
            recommendation="Repair task JSON files until tools/validate_guardrails.py passes.",
        )


def placeholder_summary(text: str) -> tuple[int, list[str]]:
    patterns = [
        r"\bTODO\b",
        r"Status:\s*placeholder",
        r"Status:\s*project-specific placeholder",
        r"\bFill later\b",
    ]
    matches: list[str] = []
    for pattern in patterns:
        count = len(re.findall(pattern, text, flags=re.IGNORECASE))
        if count:
            matches.append(f"{pattern}: {count}")
    return sum(int(item.rsplit(": ", 1)[1]) for item in matches), matches


def collect_placeholder_findings(findings: list[Finding], docs: list[Path]) -> None:
    for path in docs:
        if "docs/exec-plans/completed" in relative(path):
            continue
        total, matches = placeholder_summary(read_text(path))
        if total:
            severity = "medium" if relative(path) in {"ARCHITECTURE.md", "docs/RUNTIME.md", "docs/GUARDRAILS.md"} else "low"
            add_finding(
                findings,
                severity=severity,
                dimension="knowledge system",
                category="doc-placeholder",
                title=f"Placeholder language remains in {relative(path)}",
                detail="; ".join(matches),
                paths=[path],
                control="Documentation placeholder scan",
                recommendation="Resolve concrete harness placeholders now; keep only product-specific placeholders that cannot be known yet.",
            )


def normalize_heading(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def collect_duplicate_heading_findings(findings: list[Finding], docs: list[Path]) -> None:
    headings: dict[str, list[tuple[Path, str]]] = {}
    for path in docs:
        if "docs/exec-plans/completed" in relative(path):
            continue
        for line in read_text(path).splitlines():
            match = re.match(r"^(#{2,6})\s+(.+?)\s*$", line)
            if not match:
                continue
            title = match.group(2).strip()
            normalized = normalize_heading(title)
            if normalized in COMMON_HEADINGS or not normalized:
                continue
            headings.setdefault(normalized, []).append((path, title))

    for normalized, entries in sorted(headings.items()):
        paths = sorted({path for path, _ in entries})
        if len(paths) < 2:
            continue
        title = entries[0][1]
        add_finding(
            findings,
            severity="low",
            dimension="knowledge system",
            category="doc-overlap",
            title=f"Repeated documentation heading: {title}",
            detail="The same heading appears in multiple docs and may need a canonical owner.",
            paths=paths,
            control="Duplicate heading scan",
            recommendation="Keep one canonical definition and replace secondary copies with short summaries or links.",
        )


def is_external_reference(target: str) -> bool:
    lowered = target.lower()
    return (
        not target
        or lowered.startswith("http://")
        or lowered.startswith("https://")
        or lowered.startswith("mailto:")
        or lowered.startswith("#")
        or "<" in target
        or ">" in target
        or "*" in target
    )


def resolve_reference(source: Path, target: str) -> Path | None:
    cleaned = target.strip().strip("<>").split("#", 1)[0].strip()
    if is_external_reference(cleaned):
        return None
    cleaned = cleaned.replace("\\", "/")
    if cleaned.startswith("/"):
        return ROOT / cleaned.lstrip("/")
    first = cleaned.split("/", 1)[0]
    if first in TOP_LEVEL_PATHS:
        return ROOT / cleaned
    return source.parent / cleaned


def code_span_path_candidates(value: str) -> list[str]:
    candidates: list[str] = []
    pattern = (
        r"(?:AGENTS\.md|ARCHITECTURE\.md|PLANS\.md|README\.md|"
        r"(?:artifacts|docs|evals|references|runtime|tools)/[A-Za-z0-9_./-]+)"
    )
    for match in re.findall(pattern, value.replace("\\", "/")):
        candidates.append(match)
    return candidates


def collect_reference_findings(findings: list[Finding], docs: list[Path]) -> None:
    seen: set[tuple[str, str]] = set()
    missing: dict[str, list[Path]] = {}
    for path in docs:
        if "docs/exec-plans/completed" in relative(path):
            continue
        text = read_text(path)
        targets = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
        for code_span in re.findall(r"`([^`]+)`", text):
            targets.extend(code_span_path_candidates(code_span))

        for target in targets:
            resolved = resolve_reference(path, target)
            if resolved is None:
                continue
            key = (relative(path), target)
            if key in seen:
                continue
            seen.add(key)
            if not resolved.exists():
                missing.setdefault(target, []).append(path)

    for target, paths in sorted(missing.items()):
        add_finding(
            findings,
            severity="medium",
            dimension="knowledge system",
            category="doc-reference",
            title=f"Missing local reference: {target}",
            detail=f"{len(paths)} document(s) reference {target}, but the path was not found.",
            paths=sorted(set(paths)),
            control="Markdown and code-span local reference scan",
            recommendation="Create the referenced file, correct the path, or mark it clearly as a future placeholder.",
        )


def collect_tool_doc_findings(findings: list[Finding], docs: list[Path]) -> None:
    docs_text = "\n".join(read_text(path) for path in docs if "docs/exec-plans" not in relative(path))
    for tool in sorted((ROOT / "tools").glob("*.py")):
        name = relative(tool)
        if name not in docs_text:
            add_finding(
                findings,
                severity="medium",
                dimension="knowledge system",
                category="tool-doc-drift",
                title=f"Tool is not documented: {name}",
                detail="Every harness tool should be discoverable from runtime, guardrail, operation, or evaluation docs.",
                paths=[tool],
                control="Tool documentation coverage scan",
                recommendation="Document the tool's purpose, invocation mode, and artifact behavior.",
            )


def collect_code_quality_findings(findings: list[Finding]) -> None:
    for path in sorted((ROOT / "tools").glob("*.py")):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            add_finding(
                findings,
                severity="high",
                dimension="runtime",
                category="code-quality",
                title=f"Python compile failed for {relative(path)}",
                detail=str(exc),
                paths=[path],
                control="py_compile",
                recommendation="Fix syntax or import-time code issues before running the harness.",
            )

        text = read_text(path)
        if "if __name__ == \"__main__\":" not in text:
            add_finding(
                findings,
                severity="low",
                dimension="runtime",
                category="code-quality",
                title=f"Tool has no command-line entrypoint: {relative(path)}",
                detail="Repository tools should be directly runnable unless they are explicitly helper modules.",
                paths=[path],
                control="Tool entrypoint scan",
                recommendation="Add an entrypoint or document that the file is helper-only.",
            )


def load_task(path: Path) -> dict[str, Any] | None:
    try:
        task = json.loads(read_text(path))
    except json.JSONDecodeError:
        return None
    return task if isinstance(task, dict) else None


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def collect_task_health_findings(findings: list[Finding], stale_days: int) -> None:
    now = datetime.now(timezone.utc)
    queued_titles: dict[str, list[Path]] = {}
    for state_dir in ("queue", "active", "blocked", "completed"):
        directory = TASK_ROOT / state_dir
        for path in sorted(directory.glob("*.json")):
            if path.name == "example-task.json":
                continue
            task = load_task(path)
            if task is None:
                continue
            title = str(task.get("title", "")).strip().lower()
            if state_dir == "queue" and title:
                queued_titles.setdefault(title, []).append(path)

            updated = parse_time(task.get("updated_at") or task.get("created_at"))
            if state_dir == "active" and updated is not None and (now - updated).days >= stale_days:
                add_finding(
                    findings,
                    severity="medium",
                    dimension="operations",
                    category="task-health",
                    title=f"Active task is stale: {task.get('id', path.stem)}",
                    detail=f"Task has been active for at least {stale_days} days.",
                    paths=[path],
                    control="Task state age scan",
                    recommendation="Resume, complete, or move the task to blocked with evidence.",
                )
            if state_dir == "blocked" and not task.get("artifacts"):
                add_finding(
                    findings,
                    severity="medium",
                    dimension="operations",
                    category="task-health",
                    title=f"Blocked task has no evidence: {task.get('id', path.stem)}",
                    detail="Blocked tasks should link to the run or artifact that explains the blocker.",
                    paths=[path],
                    control="Blocked task evidence scan",
                    recommendation="Attach artifacts or notes that explain the human action required.",
                )

    for title, paths in queued_titles.items():
        if len(paths) > 1:
            add_finding(
                findings,
                severity="low",
                dimension="operations",
                category="task-health",
                title=f"Duplicate queued task title: {title}",
                detail="Queued tasks with the same title may be duplicate work.",
                paths=paths,
                control="Queued task duplicate scan",
                recommendation="Merge or rename tasks so the queue remains legible.",
            )


def collect_artifact_findings(findings: list[Finding]) -> None:
    runs_dir = ROOT / "artifacts" / "runs"
    if not runs_dir.exists():
        return
    for run_dir in sorted(path for path in runs_dir.iterdir() if path.is_dir()):
        summary = run_dir / "summary.json"
        if not summary.exists():
            add_finding(
                findings,
                severity="medium",
                dimension="observability",
                category="artifact-hygiene",
                title=f"Run artifact has no summary: {run_dir.name}",
                detail="Every harness run directory should include summary.json for later agent inspection.",
                paths=[run_dir],
                control="Run artifact summary scan",
                recommendation="Add the missing summary if recoverable, or archive the orphaned run directory.",
            )
            continue
        try:
            data = json.loads(read_text(summary))
        except json.JSONDecodeError as exc:
            add_finding(
                findings,
                severity="high",
                dimension="observability",
                category="artifact-hygiene",
                title=f"Run summary is invalid JSON: {run_dir.name}",
                detail=str(exc),
                paths=[summary],
                control="Run summary JSON parse",
                recommendation="Repair or archive the invalid summary artifact.",
            )
            continue
        for field in ("run_id", "task_id", "results"):
            if field not in data:
                add_finding(
                    findings,
                    severity="medium",
                    dimension="observability",
                    category="artifact-hygiene",
                    title=f"Run summary missing field: {field}",
                    detail=f"{relative(summary)} does not include {field}.",
                    paths=[summary],
                    control="Run summary schema scan",
                    recommendation="Regenerate or repair the summary so later agents can inspect the run.",
                )


def collect_eval_findings(findings: list[Finding]) -> None:
    benchmark_paths = sorted((ROOT / "evals" / "benchmarks").glob("*/benchmark.json"))
    baseline_dir = ROOT / "evals" / "baselines"
    suites: set[str] = set()
    for path in benchmark_paths:
        try:
            benchmark = json.loads(read_text(path))
        except json.JSONDecodeError as exc:
            add_finding(
                findings,
                severity="high",
                dimension="evaluation",
                category="eval-health",
                title=f"Benchmark JSON is invalid: {relative(path)}",
                detail=str(exc),
                paths=[path],
                control="Benchmark parse scan",
                recommendation="Repair benchmark JSON before running evals.",
            )
            continue
        suite = benchmark.get("suite")
        if isinstance(suite, str) and suite:
            suites.add(suite)

    for suite in sorted(suites):
        baseline = baseline_dir / f"{suite}.json"
        if not baseline.exists():
            add_finding(
                findings,
                severity="medium",
                dimension="evaluation",
                category="eval-health",
                title=f"Eval suite has no baseline: {suite}",
                detail=f"Expected {relative(baseline)}.",
                paths=[baseline],
                control="Eval baseline coverage scan",
                recommendation="Run the suite after a known-good pass with --update-baseline.",
            )

    results = sorted((ROOT / "evals" / "results").glob("*.json"))
    if benchmark_paths and not results:
        add_finding(
            findings,
            severity="low",
            dimension="evaluation",
            category="eval-health",
            title="No eval result history found",
            detail="Eval benchmarks exist, but evals/results has no JSON result files.",
            paths=["evals/results"],
            control="Eval result history scan",
            recommendation="Run python tools/run_evals.py --suite smoke and preserve the result artifact.",
        )


def collect_findings(stale_days: int) -> list[Finding]:
    findings: list[Finding] = []
    docs = markdown_files()
    collect_structure_findings(findings)
    collect_placeholder_findings(findings, docs)
    collect_duplicate_heading_findings(findings, docs)
    collect_reference_findings(findings, docs)
    collect_tool_doc_findings(findings, docs)
    collect_code_quality_findings(findings)
    collect_task_health_findings(findings, stale_days)
    collect_artifact_findings(findings)
    collect_eval_findings(findings)
    return sorted(findings, key=lambda item: (-SEVERITY_ORDER[item.severity], item.dimension, item.category, item.id))


def score_dimensions(findings: list[Finding]) -> dict[str, int]:
    dimensions = {
        "runtime": 100,
        "knowledge system": 100,
        "observability": 100,
        "guardrails": 100,
        "evaluation": 100,
        "operations": 100,
    }
    penalties = {dimension: 0 for dimension in dimensions}
    for finding in findings:
        if finding.dimension in penalties:
            penalties[finding.dimension] += SEVERITY_WEIGHTS[finding.severity]
    return {dimension: max(0, value - penalties[dimension]) for dimension, value in dimensions.items()}


def build_report(findings: list[Finding]) -> dict[str, Any]:
    scores = score_dimensions(findings)
    overall = round(sum(scores.values()) / len(scores))
    counts = {severity: 0 for severity in SEVERITY_ORDER}
    for finding in findings:
        counts[finding.severity] += 1
    return {
        "schema_version": 1,
        "id": f"{utc_stamp()}-entropy-control",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "needs_attention" if any(f.severity in {"high", "medium"} for f in findings) else "passed",
        "counts": counts,
        "quality_score": {"overall": overall, **scores},
        "findings": [asdict(finding) for finding in findings],
    }


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Entropy Control Report",
        "",
        f"- ID: `{report['id']}`",
        f"- Status: `{report['status']}`",
        f"- Created: `{report['created_at']}`",
        f"- Overall score: `{report['quality_score']['overall']}`",
        "",
        "## Scores",
        "",
    ]
    for dimension, score in report["quality_score"].items():
        if dimension == "overall":
            continue
        lines.append(f"- {dimension}: {score}")
    lines.extend(["", "## Findings", ""])
    if not report["findings"]:
        lines.append("No findings.")
    for finding in report["findings"]:
        paths = ", ".join(f"`{path}`" for path in finding["paths"]) or "`repo`"
        lines.extend(
            [
                f"### {finding['severity'].upper()}: {finding['title']}",
                "",
                f"- Dimension: {finding['dimension']}",
                f"- Category: {finding['category']}",
                f"- Paths: {paths}",
                f"- Control: {finding['control']}",
                f"- Detail: {finding['detail']}",
                f"- Recommendation: {finding['recommendation']}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def task_from_finding(finding: dict[str, Any], report_path: Path) -> dict[str, Any]:
    task_id = f"entropy-{finding['id']}"
    task_id = re.sub(r"[^a-z0-9-]+", "-", task_id.lower()).strip("-")[:64].strip("-")
    prompt = (
        f"Address entropy finding `{finding['id']}` from {relative(report_path)}.\n\n"
        f"Title: {finding['title']}\n"
        f"Detail: {finding['detail']}\n"
        f"Paths: {', '.join(finding['paths']) or 'repo'}\n"
        f"Recommendation: {finding['recommendation']}\n\n"
        "Make the smallest repo-legible change that resolves the finding. "
        "Preserve product-specific placeholders when the framework cannot know the answer yet, "
        "but mark them clearly as intentional."
    )
    return {
        "id": task_id,
        "title": f"Resolve entropy finding: {finding['title']}",
        "status": "queued",
        "priority": 80 if finding["severity"] == "high" else 90,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "prompt": prompt,
        "acceptance": [
            "The finding is resolved or explicitly documented as intentional.",
            "Entropy control produces no equivalent high or medium finding for the same issue.",
        ],
        "validation_commands": [
            "python tools/entropy_control.py --report",
            "python tools/validate_harness_structure.py",
        ],
        "commit_policy": "never",
        "run_ids": [],
        "artifacts": [relative(report_path)],
        "notes": "Generated by tools/entropy_control.py.",
    }


def queue_tasks(report: dict[str, Any], report_path: Path, include_low: bool) -> list[str]:
    created: list[str] = []
    allowed = {"high", "medium"} if not include_low else {"high", "medium", "low"}
    for finding in report["findings"]:
        if finding["severity"] not in allowed:
            continue
        task = task_from_finding(finding, report_path)
        path = QUEUE_DIR / f"{task['id']}.json"
        if path.exists():
            continue
        write_json(path, task)
        created.append(relative(path))
    return created


def update_quality_score(report: dict[str, Any], report_path: Path) -> None:
    score = report["quality_score"]
    debt = [
        finding
        for finding in report["findings"]
        if finding["severity"] in {"high", "medium"}
    ]
    lines = [
        "# Quality Score",
        "",
        "Status: generated by entropy control.",
        "",
        "Use this document to track recurring quality signals for the harness and the project it supports.",
        "",
        "## Current Score",
        "",
        f"- Overall: {score['overall']}",
        f"- Runtime: {score['runtime']}",
        f"- Knowledge system: {score['knowledge system']}",
        f"- Observability: {score['observability']}",
        f"- Guardrails: {score['guardrails']}",
        f"- Evaluation: {score['evaluation']}",
        f"- Operations: {score['operations']}",
        "",
        "## Scoring Notes",
        "",
        f"Last updated from `{relative(report_path)}`.",
        "Scores start at 100 per dimension and subtract deterministic entropy penalties.",
        "",
        "## Open Quality Debt",
        "",
    ]
    if not debt:
        lines.append("- None recorded.")
    else:
        for finding in debt:
            paths = ", ".join(f"`{path}`" for path in finding["paths"]) or "`repo`"
            lines.append(f"- {finding['severity']}: {finding['title']} ({paths})")
    QUALITY_SCORE_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_report(report: dict[str, Any]) -> tuple[Path, Path]:
    MAINTENANCE_DIR.mkdir(parents=True, exist_ok=True)
    base = MAINTENANCE_DIR / report["id"]
    json_path = base.with_suffix(".json")
    md_path = base.with_suffix(".md")
    write_json(json_path, report)
    md_path.write_text(markdown_report(report), encoding="utf-8")
    return json_path, md_path


def copy_latest(report_path: Path) -> None:
    latest = MAINTENANCE_DIR / "latest-entropy-report.json"
    if report_path.exists():
        shutil.copyfile(report_path, latest)


def should_fail(report: dict[str, Any], threshold: str) -> bool:
    if threshold == "none":
        return False
    required = SEVERITY_ORDER[threshold]
    return any(SEVERITY_ORDER[finding["severity"]] >= required for finding in report["findings"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run harness entropy control checks.")
    parser.add_argument("--report", action="store_true", help="Write JSON and Markdown entropy reports.")
    parser.add_argument("--queue-tasks", action="store_true", help="Create queued cleanup tasks for high/medium findings.")
    parser.add_argument("--include-low-tasks", action="store_true", help="Also queue low-severity findings.")
    parser.add_argument("--update-quality-score", action="store_true", help="Rewrite docs/QUALITY_SCORE.md from the report.")
    parser.add_argument("--stale-days", type=int, default=14, help="Age threshold for stale active tasks.")
    parser.add_argument("--fail-on", choices=("none", "low", "medium", "high"), default="none")
    args = parser.parse_args(argv)

    if not args.report and not args.queue_tasks and not args.update_quality_score:
        args.report = True

    findings = collect_findings(stale_days=args.stale_days)
    report = build_report(findings)
    json_path, md_path = write_report(report)
    copy_latest(json_path)

    queued: list[str] = []
    if args.queue_tasks:
        queued = queue_tasks(report, json_path, args.include_low_tasks)
        report["queued_tasks"] = queued
        write_json(json_path, report)
        md_path.write_text(markdown_report(report), encoding="utf-8")
        copy_latest(json_path)

    if args.update_quality_score:
        update_quality_score(report, json_path)

    print(f"Entropy report: {relative(json_path)}")
    print(f"Entropy markdown: {relative(md_path)}")
    print(f"Status: {report['status']}")
    print(f"Findings: {len(report['findings'])}")
    if queued:
        print(f"Queued tasks: {len(queued)}")

    return 1 if should_fail(report, args.fail_on) else 0


if __name__ == "__main__":
    sys.exit(main())
