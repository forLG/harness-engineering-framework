# Guardrails

Status: initial scaffold.

Record architecture, style, safety, and operational rules that should become mechanical checks.

## Structural Rules

- Required files and directories are checked by `tools/validate_harness_structure.py`.
- The outer loop task state must live under `runtime/tasks/`.
- Role definitions must live under `docs/agent-roles/`.
- Run evidence must live under `artifacts/runs/`.
- Architecture boundaries: TODO, fill when applied to a real project.
- Naming invariants: task ids should be short, lowercase, and stable.
- File-size invariants: `AGENTS.md` must stay under the validator limit.

## Tool Rules

- Allowed tools: repository-local reads, edits, local validation commands, artifact writes.
- Conditionally allowed tools: local `git add --all .` and `git commit` after a successful Ralph loop run when auto-commit is explicitly enabled.
- Restricted tools: production changes, credential access, destructive filesystem operations, external service mutation, automatic pushes, automatic merges.
- Escalation-required tools: anything outside the local harness permission model or requiring secrets.

## Git Commit Guardrails

- Auto-commit requires a clean worktree before the task starts.
- Auto-commit must run after validation and review, not before.
- Auto-commit must not include remote mutation such as `git push`.
- Auto-commit failures should leave evidence in the run output and require human follow-up.

## Documentation Rules

- `AGENTS.md` must remain concise.
- Durable knowledge belongs in focused docs.
- Active execution plans belong in `docs/exec-plans/active/`.
- Role-specific behavior belongs in `docs/agent-roles/`, not in `AGENTS.md`.
- Machine-readable task state belongs in JSON files under `runtime/tasks/`.
- Maintenance automation belongs to Milestone 5 and must not be added to the Milestone 2 Ralph loop.

## Future Checks

- Dependency boundary checker:
- Task schema checker:
- Stale documentation checker:
- Quality score updater:
- Eval regression gate:
