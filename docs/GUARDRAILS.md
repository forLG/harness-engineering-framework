# Guardrails

Status: initial scaffold.

Record architecture, style, safety, and operational rules that should become mechanical checks.

## Structural Rules

- Required files and directories are checked by `tools/validate_harness_structure.py`.
- Task JSON schema, status-directory alignment, task id naming, and filename/id matching are checked by `tools/validate_guardrails.py`.
- The outer loop task state must live under `runtime/tasks/`.
- Role definitions must live under `docs/agent-roles/`.
- Run evidence must live under `artifacts/runs/`.
- Naming invariants: task ids should be short, lowercase, and stable.
- File-size invariants: `AGENTS.md` must stay under the validator limit.

## Product-Specific Guardrails

Status: project-specific placeholder.

Fill these sections only when applying the framework to a real repository. The generic framework should provide the enforcement pattern, not invent product facts.

### Dependency Boundaries

Status: project-specific placeholder.

Define allowed and forbidden dependencies, then encode them as a mechanical check.

Fill later:

- `TODO: allowed imports between source layers or packages.`
- `TODO: forbidden imports between source layers or packages.`
- `TODO: generated file paths and edit policy.`
- `TODO: dependency-boundary exceptions and their owners.`

Mechanical check location:

- `TODO: tools/check_dependency_boundaries.py, existing linter config, or CI import-boundary rule.`

### Changed-File Requirements

Status: project-specific placeholder.

Define validation commands required by changed paths.

Fill later:

- `TODO: frontend or UI changes require build, lint, and UI verification.`
- `TODO: API or contract changes require contract tests.`
- `TODO: database migration changes require migration validation.`
- `TODO: security-sensitive changes require reviewer or human approval.`

Mechanical check location:

- `TODO: tools/check_changed_file_requirements.py or CI path filter.`

### Product Safety Rules

Status: project-specific placeholder.

Define product-specific restrictions that require escalation or special evidence.

Fill later:

- `TODO: production mutation restrictions.`
- `TODO: credential, secret, and environment-variable handling rules.`
- `TODO: deployment approval rules.`
- `TODO: external service mutation rules.`

Mechanical check location:

- `TODO: docs/SECURITY.md, tools/check_product_safety.py, CI policy gate, or deployment workflow.`

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

- Dependency boundary checker: project-specific placeholder.
- Task schema checker: implemented in `tools/validate_guardrails.py`.
- Changed-file requirement checker: project-specific placeholder.
- Product safety checker: project-specific placeholder.
- Stale documentation checker:
- Quality score updater:
- Eval regression gate:
