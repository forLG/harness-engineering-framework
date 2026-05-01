# Operations

Status: initial scaffold.

Define how the harness changes safely over time.

## Merge Philosophy

- Small, reviewable changes.
- Evidence attached to substantial changes.
- Mechanical checks before merge.
- Automatic local commits are allowed only after validation passes and review approves.

## Reviewer Agents

Agent review stages are defined in `docs/agent-roles/`.

- Implementer: may edit files and run safe local checks, but should not create commits.
- Validator: should not edit files; verifies reproducibility.
- Reviewer: should not edit files; reviews task result and artifacts.
- Follow-up planner: should not edit product files; creates new queued tasks.
- Maintenance planner: should not edit product files or delete artifacts; turns entropy reports into narrow cleanup tasks or human-escalation notes.

Humans still own product judgment, credentials, production changes, destructive operations, and ambiguous policy decisions.

## Automatic Commit Policy

The Ralph loop may create local Git commits when `tools/harness_loop.py` is run with `--auto-commit` or when a task declares `"commit_policy": "on_success"`.

Rules:

- Commit only successful runs: implementer completed, validator passed, reviewer approved, and no follow-up work is needed.
- Require a clean Git worktree before the task starts.
- Commit with `git add --all .` followed by `git commit`.
- Never push, merge, tag, or modify remote branches automatically.
- Treat Git identity, hook failures, conflicts, and dirty preflight as human-escalation cases.

## Cleanup Loop

Recurring cleanup uses `tools/entropy_control.py`.

Manual report:

```bash
python tools/entropy_control.py --report
```

Report plus queued cleanup tasks:

```bash
python tools/entropy_control.py --report --queue-tasks
```

Report plus quality score refresh:

```bash
python tools/entropy_control.py --report --update-quality-score
```

The cleanup loop scans for:

- Stale docs.
- Documentation overlap and broken local references.
- Bad harness code, starting with Python compile failures in `tools/*.py`.
- Dead plans.
- Drift from architecture.
- Missing eval coverage.
- Accumulated artifacts that should be summarized or archived.

The cleanup loop controls entropy by reporting findings, writing evidence to `artifacts/maintenance/`, optionally creating queued tasks, and leaving implementation to the normal agent review flow. Automatic cleanup is opt-in through `tools/harness_loop.py --entropy-control report` or `--entropy-control queue-tasks`; direct deletion or broad rewriting still requires human judgment.

## Technical Debt

Record debt in execution plans or project issue tracking. Keep enough context for another agent to resume work.
