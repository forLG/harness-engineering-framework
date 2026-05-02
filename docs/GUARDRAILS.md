# Guardrails

Status: scaffold.

Record architecture, style, safety, and operational rules that should become mechanical checks.

## Structural Rules

- Required files and directories are checked by `tools/validate_harness_structure.py`.
- Task JSON schema, status-directory alignment, task id naming, and filename/id matching are checked by `tools/validate_guardrails.py`.
- Entropy control findings are checked by `tools/entropy_control.py`.
- The outer loop task state must live under `runtime/tasks/`.
- Role definitions must live under `docs/agent-roles/`.
- Run evidence must live under `artifacts/runs/`.
- Maintenance evidence must live under `artifacts/maintenance/`.
- Naming invariants: task ids should be short, lowercase, and stable.
- File-size invariants: `AGENTS.md` must stay under the validator limit.

## Product-Specific Guardrails

Status: project-specific.

Fill these sections only when applying the framework to a real repository. The generic framework should provide the enforcement pattern, not invent product facts.

### Dependency Boundary Checks

Status: project-specific.

Define allowed and forbidden dependencies, then encode them as a mechanical check.

Project placeholders:

- `PROJECT_PLACEHOLDER(allowed-imports): allowed imports between source layers or packages.`
- `PROJECT_PLACEHOLDER(forbidden-imports): forbidden imports between source layers or packages.`
- `PROJECT_PLACEHOLDER(generated-file-policy): generated file paths and edit policy.`
- `PROJECT_PLACEHOLDER(dependency-exceptions): dependency-boundary exceptions and their owners.`

Mechanical check location:

- `PROJECT_PLACEHOLDER(dependency-boundary-check): repository-local checker path, existing linter config, or CI import-boundary rule.`

### Changed-File Requirements

Status: project-specific.

Define validation commands required by changed paths.

Project placeholders:

- `PROJECT_PLACEHOLDER(frontend-validation): frontend or UI changes require build, lint, and UI verification.`
- `PROJECT_PLACEHOLDER(api-validation): API or contract changes require contract tests.`
- `PROJECT_PLACEHOLDER(migration-validation): database migration changes require migration validation.`
- `PROJECT_PLACEHOLDER(security-review): security-sensitive changes require reviewer or human approval.`

Mechanical check location:

- `PROJECT_PLACEHOLDER(changed-file-check): repository-local checker path or CI path filter.`

### Product Safety Rules

Status: project-specific.

Define product-specific restrictions that require escalation or special evidence.

Project placeholders:

- `PROJECT_PLACEHOLDER(production-mutations): production mutation restrictions.`
- `PROJECT_PLACEHOLDER(secret-handling): credential, secret, and environment-variable handling rules.`
- `PROJECT_PLACEHOLDER(deployment-approval): deployment approval rules.`
- `PROJECT_PLACEHOLDER(external-service-mutations): external service mutation rules.`

Mechanical check location:

- `PROJECT_PLACEHOLDER(product-safety-check): docs/SECURITY.md section, repository-local checker path, CI policy gate, or deployment workflow.`

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
- Status, placeholder, and framework work language must follow `docs/product-specs/language-conventions.md`.
- Active execution plans belong in `docs/exec-plans/active/`.
- Role-specific behavior belongs in `docs/agent-roles/`, not in `AGENTS.md`.
- Machine-readable task state belongs in JSON files under `runtime/tasks/`.
- Maintenance automation belongs to Milestone 5 and must not be added to the Milestone 2 Ralph loop.

## Future Checks

- Dependency boundary checker: `PROJECT_PLACEHOLDER(dependency-boundary-check): choose or create the project-specific enforcement mechanism.`
- Task schema checker: implemented in `tools/validate_guardrails.py`.
- Changed-file requirement checker: `PROJECT_PLACEHOLDER(changed-file-check): choose or create the project-specific enforcement mechanism.`
- Product safety checker: `PROJECT_PLACEHOLDER(product-safety-check): choose or create the project-specific enforcement mechanism.`
- Stale documentation checker: implemented for harness docs in `tools/entropy_control.py`; product-specific freshness rules are added after framework adoption.
- Documentation overlap and broken-reference checker: implemented for repository-local Markdown in `tools/entropy_control.py`.
- Harness code quality checker: implemented for `tools/*.py` compile health in `tools/entropy_control.py`.
- Quality score updater: implemented by `tools/entropy_control.py --update-quality-score`.
- Eval regression gate: implemented by `tools/run_evals.py`.
