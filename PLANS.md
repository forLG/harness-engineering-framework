# Plans

Status: scaffold.

This file is the plan index. Keep active execution detail in `docs/exec-plans/active/` and completed plans in `docs/exec-plans/completed/`.

For the open-source framework, this document tracks framework work. When the scaffold is copied into a real project, keep the structure but replace the applied project section with repository-grounded milestones. Do not invent a fictional app roadmap in the framework repository.

## Current Framework Roadmap

Status: implemented.

### Milestone 1: Framework Skeleton

Status: implemented.

Goal: establish a repo-legible harness foundation with short entry points, durable docs, placeholder directories, and a structural validator.

Acceptance criteria:

- `AGENTS.md` maps the repository and stays concise.
- `ARCHITECTURE.md` names runtime core and extension points.
- `docs/` contains quality, reliability, security, guardrail, observability, evaluation, and operations placeholders.
- `tools/validate_harness_structure.py` verifies required paths.

### Milestone 2: Runtime Prototype

Status: implemented.

Goal: implement the minimal Ralph-style outer task loop.

Acceptance criteria:

- Task state is externalized under `runtime/tasks/`.
- Role prompts exist for implementer, validator, reviewer, and follow-up planner agents.
- `tools/harness_loop.py --once` previews the assembled prompts.
- `tools/harness_loop.py --once --execute` can run one queued task through Codex.
- Run outputs are saved under `artifacts/runs/`.
- Follow-up tasks can be generated into `runtime/tasks/queue/`.
- Successful runs can optionally create local Git commits after validation and review.
- Logs and artifacts are inspectable.
- One benchmark task runs end to end.

### Milestone 3: Mechanical Guardrails

Status: implemented.

Goal: convert architecture and quality rules into checks.

Acceptance criteria:

- Task schema and task state-directory alignment are checked.
- Task id naming and filename/id matching are checked.
- Guardrail failures include remediation guidance.
- Dependency boundaries are checked.
- Documentation freshness is checked.
- File and naming invariants are checked.

### Milestone 4: Evaluation Loop

Status: implemented.

Goal: add repeatable evals with cost, latency, and quality reporting.

Acceptance criteria:

- Benchmark tasks are versioned under `evals/benchmarks/`.
- `tools/run_evals.py --suite smoke` runs deterministic local smoke benchmarks.
- Suite baselines are versioned under `evals/baselines/`.
- Eval results are stored in `evals/results/`.
- Regressions against the current baseline are visible before merge through a nonzero eval runner exit code.
- Cost fields are recorded as `null` until execute-mode benchmarks can measure model usage.
- Product-specific evals have a template under `evals/benchmarks/product-template/` but are not runnable until a target project fills them.

### Milestone 5: Entropy Control

Status: implemented.

Goal: add recurring maintenance for stale docs, drift, and quality debt.

Acceptance criteria:

- Quality score is updated on a schedule or command.
- Stale docs, documentation overlap, broken local references, and bad harness code are detected.
- Cleanup tasks are proposed as plans or queued harness tasks.
- Maintenance reports are preserved under `artifacts/maintenance/`.
- Entropy control can run manually and can be invoked automatically by the supervisor on an opt-in cadence.

## Applied Project Plan Template

Use this section only after copying the framework into a target repository. Replace these entries with facts discovered from that project.

### Milestone 1: Project Harness Orientation

Status: project-specific.

Goal: `PROJECT_PLACEHOLDER(first-project-milestone-goal): define the first realistic milestone for applying the harness to this repository.`

Acceptance criteria:

- `PROJECT_PLACEHOLDER(project-orientation): AGENTS.md, ARCHITECTURE.md, and docs/ENVIRONMENT.md reflect the target repository's actual structure, setup, and validation commands.`
- `PROJECT_PLACEHOLDER(project-validation): the target project's normal validation commands are documented and at least one safe command has been run.`
- `PROJECT_PLACEHOLDER(project-evidence): useful setup, validation, or failure evidence is preserved under artifacts/ when it explains a decision.`
