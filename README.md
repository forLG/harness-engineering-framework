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
- A repo-local Codex skill in `.skills/apply-harness-framework/` that guides the scaffold adoption workflow.

## Apply It To A Real Project

The recommended adoption model is phase-by-phase, guided by the repo-local skill in `.skills/apply-harness-framework/`.

Do not ask Codex to fill every placeholder from one giant prompt and then trust the result. A single prompt is useful as an entry point, but the actual work should inspect the target repository, fill facts from evidence, preserve unknowns as explicit placeholders, and validate after each meaningful phase.

### The Three Adoption Options

There are three practical ways to use this scaffold:

1. Manual phase filling.
   This is safest when the project is sensitive or poorly documented. A human fills each document after inspecting the repository. It is accurate but slow.

2. A single start prompt.
   This is fastest for demos and prototypes. It can produce a useful first draft, but it is more likely to invent commands, architecture, owners, or policies.

3. Skill-guided phased adoption.
   This is the recommended path. The `.skills/apply-harness-framework/` skill gives Codex the workflow, fill order, evidence rules, validation steps, and reporting format. Codex still works phase by phase, but the process is repeatable and easier for new users.

In short: use a start prompt to launch the work, use the skill to guide the process, and use phases to keep the result trustworthy.

### Copy The Framework

Copy this framework into the root of the target project. The target project should then contain the top-level files and directories from this scaffold, including:

- `AGENTS.md`
- `ARCHITECTURE.md`
- `PLANS.md`
- `README.md`
- `docs/`
- `runtime/`
- `tools/`
- `evals/`
- `artifacts/`
- `.skills/`

If the target project already has files with the same names, merge carefully instead of overwriting project-specific information. Keep the target project's existing setup, architecture, and operations docs as evidence.

### Start Codex In The Target Project

Run Codex from the target repository root:

```bash
codex -C path/to/real-project
```

If your Codex environment discovers repo-local skills, invoke the skill directly:

```text
Use $apply-harness-framework to apply this scaffold to the current repository.
```

If repo-local skills are not auto-discovered, point Codex at the skill file:

```text
Read .skills/apply-harness-framework/SKILL.md and follow it to apply this harness framework to the current repository.
```

### Recommended Start Prompt

Use this as the first message after copying the scaffold:

```text
Apply the harness engineering framework in this repository to the current project.

Use .skills/apply-harness-framework/SKILL.md as the workflow.

First inspect the repository structure, build and test commands, runtime stack, docs, CI, scripts, dependency files, service configuration, and existing conventions.

Then work phase by phase. Fill only facts grounded in repository files or safe command output. Do not invent setup commands, service ports, architecture boundaries, owners, security rules, deployment rules, or validation commands.

When a fact cannot be discovered, leave PROJECT_PLACEHOLDER(<key>): <exact missing information needed and likely source>.

Keep AGENTS.md concise. Put durable detail in focused docs.

After each phase, run python tools/validate_harness_structure.py and any safe target-project validation command discovered from the repository.
```

### Adoption Phases

Phase 1 creates basic repository orientation:

- Fill `docs/ENVIRONMENT.md`.
- Fill `ARCHITECTURE.md`.
- Keep `AGENTS.md` short and project-specific.
- Outcome: a new agent can understand the repository shape and run at least one safe validation command.

Phase 2 defines how agent work runs and leaves evidence:

- Fill `docs/RUNTIME.md`.
- Fill `docs/OBSERVABILITY.md`.
- Fill `docs/RELIABILITY.md`.
- Outcome: tasks, runs, failures, logs, traces, screenshots, and validation evidence have clear homes.

Phase 3 turns expectations into safety and measurement:

- Fill `docs/GUARDRAILS.md`.
- Fill `docs/SECURITY.md`.
- Fill `docs/EVALUATION.md`.
- Fill `docs/QUALITY_SCORE.md`.
- Outcome: project rules start becoming checks, benchmark tasks, and quality signals.

Phase 4 makes the harness maintainable:

- Fill `docs/OPERATIONS.md`.
- Replace the applied-project section in `PLANS.md`.
- Add active execution plans under `docs/exec-plans/active/` when work is substantial.
- Outcome: the project has a repeatable planning, review, cleanup, and maintenance loop.

### What Codex Should Inspect

Before editing placeholders, Codex should inspect high-value repository evidence:

- File structure from `rg --files`.
- Package manifests and lockfiles.
- Build, test, lint, typecheck, and dev-server scripts.
- CI workflows and deployment configuration.
- Docker, Compose, dev container, or service definitions.
- Environment examples such as `.env.example` or `.env.sample`.
- Existing README files, architecture docs, ADRs, API docs, and runbooks.
- Test directories, fixtures, benchmark tasks, and eval files.
- Existing agent instructions such as `AGENTS.md`, `.codex/`, or `.github/`.

### What Codex Should Not Invent

Leave a `PROJECT_PLACEHOLDER(...)` when the repository does not answer the question. This is better than confident fiction.

Common facts that must be evidence-backed:

- Runtime versions.
- Dependency installation commands.
- Build, test, lint, and typecheck commands.
- Local services and ports.
- Environment variables and secret handling.
- Source layers and dependency boundaries.
- Generated files and contract files.
- Deployment process and approval rules.
- Product-specific security restrictions.
- Evaluation acceptance criteria.

### Validation During Adoption

Run the harness validator after changing framework layout or task state:

```bash
python tools/validate_harness_structure.py
```

Run entropy control when you want an adoption progress report:

```bash
python tools/entropy_control.py --report
```

Run smoke evals after changing runtime, task, or eval behavior:

```bash
python tools/run_evals.py --suite smoke
```

When applied to a real project, also run the project's own safe validation commands, such as tests, type checks, lint checks, builds, and UI verification.

## Placeholder Convention

The canonical rule is `docs/product-specs/language-conventions.md`. In short, this framework is intentionally generic. Anything that depends on the target repository uses this format:

```text
PROJECT_PLACEHOLDER(<key>): <what the adopter must discover and fill>
```

Use `PROJECT_PLACEHOLDER(...)` only for project-specific facts that the universal scaffold cannot know, such as source layers, build commands, service ports, secret handling, deployment rules, UI verification, product eval tasks, and ownership boundaries.

Known framework work that is not target-project-specific uses this separate format:

```text
FRAMEWORK_TODO(<key>): <framework improvement still needed>
```

When applying the scaffold, replace project placeholders with repository-grounded facts. If the fact cannot be discovered, leave the placeholder in place and make the missing input precise.

Entropy control records valid `PROJECT_PLACEHOLDER(...)` and `FRAMEWORK_TODO(...)` entries as an intentional placeholder inventory in its reports and summarizes them in `docs/QUALITY_SCORE.md`; they do not affect score or queued cleanup tasks.

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
Automatic commit messages use functional prefixes such as `docs:`, `feat:`, `fix:`, `test:`, or `chore:`. Tasks can set a full `commit_message` or a `commit_type` for generated messages.

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

For product-specific phase-three evals, start from `evals/benchmarks/product-template/`. Copy the template into a concrete benchmark directory, replace `PROJECT_PLACEHOLDER(...)` values with the target project's facts, run it with `--no-baseline` while calibrating, then create a baseline with `--update-baseline` after a known-good pass.

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
