# Plans

This file is the plan index. Keep active execution detail in `docs/exec-plans/active/` and completed plans in `docs/exec-plans/completed/`.

## Current Roadmap

### Milestone 1: Framework Skeleton

Status: active.

Goal: establish a repo-legible harness foundation with short entry points, durable docs, placeholder directories, and a structural validator.

Acceptance criteria:

- `AGENTS.md` maps the repository and stays concise.
- `ARCHITECTURE.md` names runtime core and extension points.
- `docs/` contains quality, reliability, security, guardrail, observability, evaluation, and operations placeholders.
- `tools/validate_harness_structure.py` verifies required paths.

### Milestone 2: Runtime Prototype

Status: placeholder.

Goal: define and implement the minimal task loop.

Acceptance criteria:

- Task state is externalized.
- Tool permissions are explicit.
- Logs and artifacts are inspectable.
- One benchmark task runs end to end.

### Milestone 3: Mechanical Guardrails

Status: placeholder.

Goal: convert architecture and quality rules into checks.

Acceptance criteria:

- Dependency boundaries are checked.
- Documentation freshness is checked.
- File and naming invariants are checked.
- Guardrail failures include remediation guidance.

### Milestone 4: Evaluation Loop

Status: placeholder.

Goal: add repeatable evals with cost, latency, and quality reporting.

Acceptance criteria:

- Benchmark tasks are versioned.
- Eval results are stored in `evals/results/`.
- Regressions are visible before merge.

### Milestone 5: Entropy Control

Status: placeholder.

Goal: add recurring maintenance for stale docs, drift, and quality debt.

Acceptance criteria:

- Quality score is updated on a schedule or command.
- Stale docs are detected.
- Cleanup tasks are proposed as plans or PRs.

## Active Plans

- None yet.

## Completed Plans

- None yet.
