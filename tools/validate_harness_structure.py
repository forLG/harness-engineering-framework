from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "AGENTS.md",
    "ARCHITECTURE.md",
    "PLANS.md",
    "docs/QUALITY_SCORE.md",
    "docs/RELIABILITY.md",
    "docs/SECURITY.md",
    "docs/GUARDRAILS.md",
    "docs/ENVIRONMENT.md",
    "docs/RUNTIME.md",
    "docs/OBSERVABILITY.md",
    "docs/EVALUATION.md",
    "docs/OPERATIONS.md",
    "docs/design-docs",
    "docs/exec-plans/active",
    "docs/exec-plans/completed",
    "docs/generated",
    "docs/product-specs",
    "docs/references",
    "references",
    "runtime",
    "tools",
    "evals/benchmarks",
    "evals/results",
    "artifacts/logs",
    "artifacts/traces",
    "artifacts/screenshots",
]

MAX_AGENTS_BYTES = 6000


def main() -> int:
    failures = []

    for relative in REQUIRED_PATHS:
        path = ROOT / relative
        if not path.exists():
            failures.append(f"missing required path: {relative}")

    agents = ROOT / "AGENTS.md"
    if agents.exists() and agents.stat().st_size > MAX_AGENTS_BYTES:
        failures.append(
            f"AGENTS.md is {agents.stat().st_size} bytes; keep it under {MAX_AGENTS_BYTES} bytes"
        )

    if failures:
        print("Harness structure validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Harness structure validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
