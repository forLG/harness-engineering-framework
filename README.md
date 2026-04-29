# Harness Engineering Framework

This repository is a universal scaffold for turning a real software project into an agent-legible harness engineering project.

The goal is not to store one large prompt. The goal is to create repository-native infrastructure that lets Codex or another agent understand the project, run tasks, validate work, preserve evidence, and improve safely over time.

## What This Framework Provides

- A short agent entry point in `AGENTS.md`.
- Architecture and planning documents at the repository root.
- Focused docs for environment, runtime, observability, guardrails, evaluation, operations, reliability, security, and quality.
- Placeholder directories for execution plans, references, generated docs, evals, runtime code, tools, and run artifacts.
- A structural validator in `tools/validate_harness_structure.py`.

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
codex exec -C path/to/real-project "Implement the active plan in docs/exec-plans/active/example.md"
```

Use JSON output when a harness runner needs to capture events:

```bash
codex exec --json -C path/to/real-project "Run the harness evaluation plan"
```

Store run outputs in:

- `artifacts/logs/`
- `artifacts/traces/`
- `artifacts/screenshots/`
- `evals/results/`

## From Documentation To Harness

The first version of a harness is usually documentation plus a few checks. A mature harness converts recurring expectations into mechanical enforcement.

Good next steps after filling placeholders:

- Add a real runner script that wraps `codex exec`.
- Add structural checks for required docs and directories.
- Add project-specific lint rules for architecture boundaries.
- Add benchmark tasks under `evals/benchmarks/`.
- Capture eval results under `evals/results/`.
- Add cleanup checks for stale docs, dead plans, and drift from architecture.

## Validation

Run the scaffold validator after changing the framework layout:

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
