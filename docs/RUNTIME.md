# Runtime

Status: initial Ralph loop scaffold.

This harness uses Codex as the worker agent and a repository-local supervisor script as the outer loop. Codex handles implementation, validation, review, and follow-up planning. The supervisor chooses queued tasks, invokes role-specific agents, captures artifacts, moves task state, and queues follow-up work.

## Invocation Modes

- Human-supervised interactive runs: `codex -C <project>`.
- One-shot non-interactive runs: `codex exec --full-auto -C <project> "<prompt>"`.
- Harness task loop preview: `python tools/harness_loop.py --once`.
- Harness task loop execution: `python tools/harness_loop.py --once --execute`.
- Harness task loop with successful-run commits: `python tools/harness_loop.py --once --execute --auto-commit`.
- Batch execution: `python tools/harness_loop.py --until-empty --execute --max-tasks 5`.
- Harness smoke evals: `python tools/run_evals.py --suite smoke`.
- Entropy report: `python tools/entropy_control.py --report`.
- Entropy report with queued cleanup tasks: `python tools/entropy_control.py --report --queue-tasks`.
- Entropy report with quality score refresh: `python tools/entropy_control.py --report --update-quality-score`.

The supervisor defaults to preview mode. It writes the prompts it would send to Codex without moving task state or invoking the agent.

When `--execute` is used, the supervisor invokes role agents with `codex exec --full-auto -C <repo> ...` by default. `--full-auto` is the sandboxed low-friction Codex mode; it is not the dangerous approval-and-sandbox bypass mode. Use `--no-codex-full-auto` when a harness run should preserve Codex's normal approval prompts instead.

## Runner Entrypoints

- `tools/harness_loop.py`: Ralph-style outer loop supervisor.
- `tools/run_evals.py`: eval runner for benchmark definitions under `evals/benchmarks/`.
- `tools/entropy_control.py`: maintenance runner for stale docs, doc overlap, bad harness code, queue health, artifact hygiene, eval drift, and quality scoring.
- `tools/validate_harness_structure.py`: structural and guardrail validator for required harness files, directories, and task state.
- `tools/validate_guardrails.py`: task schema, naming, and status-directory validator used by the structural validator.
- `runtime/tasks/TASK_SCHEMA.md`: task file contract.
- `docs/agent-roles/*.md`: role-specific responsibilities and machine-readable output contracts.

## Task Loop

The outer loop is:

1. Select the next `queued` task from `runtime/tasks/queue/`.
2. Create `artifacts/runs/<timestamp>-<task-id>/`.
3. Move the task to `runtime/tasks/active/` when `--execute` is used.
4. Invoke the implementer role with `docs/agent-roles/implementer.md`.
5. Invoke the validator role with `docs/agent-roles/validator.md`.
6. Invoke the reviewer role with `docs/agent-roles/reviewer.md`.
7. If validation fails or review requests follow-up, invoke `docs/agent-roles/followup-planner.md`.
8. Convert planner output into new task files in `runtime/tasks/queue/`.
9. Move the original task to `runtime/tasks/completed/` or `runtime/tasks/blocked/`.
10. Save `summary.json` and all role outputs under the run artifact directory.
11. When auto-commit is enabled and the run succeeded, run `git add --all .` and `git commit`.

Entropy control is outside the core implementation path by default. When `--entropy-control report` or `--entropy-control queue-tasks` is passed to `tools/harness_loop.py`, the supervisor runs `tools/entropy_control.py` after every `--entropy-every` task attempt. This supports scheduled or batch maintenance without making cleanup implicit in normal runs.

Each role must end with `HARNESS_RESULT_JSON:` followed by valid JSON. The supervisor uses that final line to decide the next state.

## Automatic Git Commits

Automatic commits are a supervisor capability, not an implementer-agent responsibility. Enable them in either of two ways:

- Pass `--auto-commit` to commit every successful task run.
- Add task metadata such as `"commit_policy": "on_success"` or `"commit_policy": {"mode": "on_success", "message": "harness: {task_id}"}`.

The loop commits only after the validator returns `passed` and the reviewer returns `approved`. It does not commit blocked runs, failed validation, or runs that created follow-up work.

Auto-commit preflight requires a clean Git worktree before the task starts. If the tree already has modified, staged, or untracked files, the supervisor stops before invoking Codex so unrelated human work is not included in the automated commit.

## Human Interaction

Humans can supervise at three points:

- Before execution: run `python tools/harness_loop.py --once` to inspect prompts.
- During execution: the supervisor defaults to Codex `--full-auto`, so safe workspace commands can run without an interactive approval prompt while still using Codex sandboxing.
- After execution: inspect `artifacts/runs/<run-id>/summary.json`, role outputs, and queued follow-up tasks.

The loop must stop or mark a task `blocked` when a role requests human escalation.

## State and Artifacts

- Task queue: `runtime/tasks/queue/`
- Active tasks: `runtime/tasks/active/`
- Completed tasks: `runtime/tasks/completed/`
- Blocked tasks: `runtime/tasks/blocked/`
- Run artifacts: `artifacts/runs/`
- Review artifacts: `artifacts/reviews/`
- Validation artifacts: `artifacts/validation/`
- Logs: `artifacts/logs/`
- Traces: `artifacts/traces/`
- Screenshots: `artifacts/screenshots/`
- Eval results: `evals/results/`
- Maintenance reports: `artifacts/maintenance/`

## Entropy Control Loop

The entropy loop has four phases:

1. Deterministic report: `tools/entropy_control.py --report` scans for documentation overlap, placeholders, broken local references, undocumented tools, Python compile failures, task queue health, run summary hygiene, eval baseline drift, and quality score inputs.
2. Queued cleanup tasks: `--queue-tasks` converts high- and medium-severity findings into normal task JSON files under `runtime/tasks/queue/`.
3. Maintenance planning: `docs/agent-roles/maintenance-planner.md` is available for semantic triage when findings need judgment, grouping, or escalation.
4. Opt-in automation: `tools/harness_loop.py --entropy-control report` or `--entropy-control queue-tasks` runs entropy control after task attempts on a configurable cadence.

The entropy tool must not silently delete artifacts, rewrite broad documentation, or mutate product code. It reports, refreshes quality scoring when explicitly requested, and queues work for the existing implementer, validator, and reviewer flow.

## Eval Loop

The eval runner stages benchmark tasks into `runtime/tasks/queue/`, gives them a high-priority value so they are selected ahead of normal work, runs the harness loop or deterministic commands, checks required artifacts, records latency and status, then removes the staged eval task.

Smoke evals run in preview mode and do not invoke Codex. By default, suite results are compared against `evals/baselines/<suite>.json`; use `--update-baseline` only after a known-good pass. Product-specific suites may add execute-mode benchmarks later, but those should define cost, latency, sandbox, and approval expectations before being used in CI.

## Stop Conditions

- Success: validator returns `passed` and reviewer returns `approved`.
- Follow-up: validator returns `failed` or reviewer returns `needs_followup`; the planner may create new queued tasks.
- Blocked: any role returns `blocked`, Codex is unavailable, auto-commit preflight fails, or required human input is needed.
- Retry: create a follow-up task instead of silently rerunning the same task.
- Timeout: TODO, add subprocess timeout and task retry metadata after the first real run.

## Open Decisions

- Codex invocation method: `codex exec --full-auto -C <repo> "<assembled prompt>"` for supervisor execute mode.
- Interactive command: `codex -C <repo>`.
- Non-interactive command: managed by `tools/harness_loop.py`.
- Approval policy: supervisor execute mode uses Codex's sandboxed `--full-auto` mode by default, plus role-level escalation rules; auto-commit is local-only and never pushes.
- JSON or trace format: role outputs use `HARNESS_RESULT_JSON`; run summary uses JSON.
- Resume strategy: continue from task files and artifacts, not hidden process memory.
