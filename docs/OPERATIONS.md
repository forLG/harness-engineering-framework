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

Status: placeholder.

Recurring cleanup should scan for:

- Stale docs.
- Dead plans.
- Drift from architecture.
- Missing eval coverage.
- Accumulated artifacts that should be summarized or archived.

## Technical Debt

Record debt in execution plans or project issue tracking. Keep enough context for another agent to resume work.
