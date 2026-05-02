# Harness Engineering Framework

This repository is a universal scaffold for turning a real software project into an agent-legible harness engineering project.

The goal is not to store one large prompt. The goal is to create repository-native infrastructure that lets Codex or another agent understand the project, run tasks, validate work, preserve evidence, and improve safely over time.

## What This Framework Provides

- A short agent entry point in `AGENTS.md`.
- Architecture and planning documents at the repository root.
- Focused docs for environment, runtime, observability, guardrails, evaluation, operations, reliability, security, and quality.
- Placeholder directories for execution plans, raw references, distilled reference notes, generated docs, evals, runtime code, tools, and run artifacts.
- A structural and guardrail validator in `tools/validate_harness_structure.py`, with task-specific checks in `tools/validate_guardrails.py`.
- A smoke evaluation runner in `tools/run_evals.py`, with starter benchmark definitions under `evals/benchmarks/`.
- An entropy control runner in `tools/entropy_control.py` for stale docs, overlap, bad harness code, queue health, artifacts, eval drift, and quality scoring.

## Apply It To A Real Project

1. Copy this framework into the root of the target project.
2. Keep `AGENTS.md` short. It should stay a map, not a full knowledge base.
3. Start Codex in the target project:

```bash
codex -C path/to/real-project
```

4. Ask Codex to inspect the repository before filling placeholders.
5. Fill only facts grounded in the repository. Leave clear TODOs for unknowns.
6. Run the structural validator and the project's normal checks.

## Starter Prompt

Use this prompt after copying the scaffold into a real project:

```text
Apply the harness engineering framework in this repository to the current project.

First inspect the repository structure, build and test commands, runtime stack, docs, CI, scripts, dependency files, service configuration, and existing conventions.

Then fill the placeholder harness files with project-specific information:
- Keep AGENTS.md concise and point to deeper docs.
- Fill ARCHITECTURE.md with actual project architecture, boundaries, runtime shape, and extension points.
- Fill docs/ENVIRONMENT.md with local setup, dependency installation, services, ports, environment variables, and reproducible commands.
- Fill docs/RUNTIME.md with how Codex or another agent should be invoked, supervised, resumed, and logged for this project.
- Fill docs/OBSERVABILITY.md with logs, traces, screenshots, metrics, browser or UI verification, and local reproduction steps.
- Fill docs/GUARDRAILS.md with rules that should become mechanical checks.
- Fill docs/EVALUATION.md with benchmark tasks, acceptance criteria, regression checks, cost reporting, and latency reporting.
- Fill docs/OPERATIONS.md with merge, review, cleanup, maintenance, and technical debt workflow.
- Fill docs/RELIABILITY.md, docs/SECURITY.md, and docs/QUALITY_SCORE.md with project-specific standards.
- Update PLANS.md with a realistic first milestone.

Do not invent facts. If something cannot be discovered, leave a TODO with the exact missing information needed.

After editing, run tools/validate_harness_structure.py and any existing project validation commands you can safely run.
```

## Suggested Fill Order

### Phase 1: Repository Discovery

Fill:

- `docs/ENVIRONMENT.md`
- `ARCHITECTURE.md`
- `AGENTS.md`

Outcome: a new agent can orient itself and run the project locally.

### Phase 2: Runtime And Observability

Fill:

- `docs/RUNTIME.md`
- `docs/OBSERVABILITY.md`
- `docs/RELIABILITY.md`

Outcome: the project has a clear model for invoking agents, capturing evidence, reproducing failures, and deciding when a run is complete.

### Phase 3: Guardrails And Evaluation

Fill:

- `docs/GUARDRAILS.md`
- `docs/EVALUATION.md`
- `docs/QUALITY_SCORE.md`

Outcome: important expectations start becoming checks, benchmarks, and measurable quality signals.

### Phase 4: Operations

Fill:

- `docs/OPERATIONS.md`
- `PLANS.md`
- `docs/exec-plans/active/`
- `docs/exec-plans/completed/`

Outcome: the project has a repeatable planning, review, cleanup, and maintenance loop.

## Interactive And Automated Runs

Use interactive Codex for human-supervised work:

```bash
codex -C path/to/real-project
```

Use non-interactive Codex for automation, CI, scheduled cleanup, or benchmark tasks:

```bash
codex exec --full-auto -C path/to/real-project "Implement the active plan in docs/exec-plans/active/<plan>.md"
```

Use JSON output when a harness runner needs to capture events:

```bash
codex exec --full-auto --json -C path/to/real-project "Run the harness evaluation plan"
```

Current supervisor runs write role prompts, role outputs, and summaries under `artifacts/runs/`.
The other artifact directories are reserved buckets for task-specific evidence and may be empty
until a project needs them:

- `artifacts/logs/`
- `artifacts/traces/`
- `artifacts/screenshots/`
- `artifacts/maintenance/`
- `evals/results/`

## References

Use `references/` for external or raw long-lived source material that agents should consult, such as copied source excerpts, vendor documentation snapshots, API specs, or source pointers.

Use `docs/references/` for project-local interpretation of those sources: distilled principles, decisions, and notes about how the material applies to this harness.

## Ralph-Style Task Loop

This scaffold includes a minimal outer loop supervisor:

```bash
python tools/harness_loop.py --once
```

Preview mode writes the implementer, validator, and reviewer prompts into `artifacts/runs/` without invoking Codex. To execute one queued task:

```bash
python tools/harness_loop.py --once --execute
```

Execute mode invokes role agents with `codex exec --full-auto -C <repo> ...`. This keeps non-interactive runs from stalling on routine permission prompts while preserving Codex sandboxing.

Queued tasks live in `runtime/tasks/queue/` as JSON files. The supervisor moves tasks through `active`, `completed`, and `blocked`, saves role outputs in `artifacts/runs/`, and can create follow-up queued tasks when validation or review finds unfinished work.

To let the loop create a local commit after a successful validated run:

```bash
python tools/harness_loop.py --once --execute --auto-commit
```

Auto-commit requires a clean Git worktree before the task starts, commits only after validator and reviewer approval, and never pushes.

## Entropy Control

Run a deterministic entropy report when the harness starts to drift:

```bash
python tools/entropy_control.py --report
```

The report checks documentation placeholders and overlap, broken local references, undocumented tools, Python compile health for harness tools, task queue health, run artifact summaries, eval baselines, and quality score inputs. It writes JSON and Markdown artifacts under `artifacts/maintenance/`.

To turn high- and medium-severity findings into normal queued tasks:

```bash
python tools/entropy_control.py --report --queue-tasks
```

To refresh `docs/QUALITY_SCORE.md` from the latest report:

```bash
python tools/entropy_control.py --report --update-quality-score
```

Entropy control is intentionally run as a standalone maintenance command rather than as part of the outer task loop.

## From Documentation To Harness

The first version of a harness is usually documentation plus a few checks. A mature harness converts recurring expectations into mechanical enforcement.

Good next steps after filling placeholders:

- Add a real runner script that wraps `codex exec`.
- Add mechanical checks for required docs, directories, and task schema rules.
- Add project-specific lint rules for architecture boundaries.
- Add benchmark tasks under `evals/benchmarks/`.
- Capture eval results under `evals/results/`.
- Add cleanup checks for stale docs, dead plans, and drift from architecture.

## Evaluation Loop

Run deterministic smoke evals before merging harness changes:

```bash
python tools/run_evals.py --suite smoke
```

The smoke suite stages benchmark tasks into `runtime/tasks/queue/`, runs the harness in preview mode, checks required artifacts, runs local validators, and writes a result file under `evals/results/`. The runner exits nonzero on failed benchmarks so regressions are visible in local checks or CI.

Smoke runs compare against `evals/baselines/smoke.json` by default. Refresh that baseline after an intentional known-good behavior change:

```bash
python tools/run_evals.py --suite smoke --update-baseline
```

List benchmark definitions:

```bash
python tools/run_evals.py --list
```

For product-specific phase-three evals, start from `evals/benchmarks/product-template/`. Copy the template into a concrete benchmark directory, fill the target project's facts, run it with `--no-baseline` while calibrating, then create a baseline with `--update-baseline` after a known-good pass.

## Validation

Run the scaffold validator after changing the framework layout or task state:

```bash
python tools/validate_harness_structure.py
```

When applied to a real project, also run the project's normal validation commands, such as tests, type checks, lint checks, build checks, and UI verification.

## Operating Principles

- Treat repository-local artifacts as the system of record.
- Keep top-level entry points short.
- Use progressive disclosure: link from maps to focused docs.
- Prefer boring, inspectable technology.
- Preserve logs, traces, screenshots, and eval results when they explain decisions.
- Convert important rules into checks instead of relying on memory.
- Separate framework concerns from product-specific workflow.
- Plan increasing autonomy in stages.
