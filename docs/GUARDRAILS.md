# Guardrails

Status: lightweight scaffold.

Record architecture, style, safety, and operational rules that Codex should preserve. Turn stable rules into scripts, lint checks, tests, or CI when feasible.

## Structural Rules

- Required files and directories are checked by `tools/validate_harness_structure.py`.
- `AGENTS.md` must remain concise.
- Durable knowledge belongs in focused docs.
- Substantial in-progress work belongs in `docs/exec-plans/active/`.
- Completed execution notes belong in `docs/exec-plans/completed/`.
- Evidence belongs under `artifacts/` only when it explains a decision, regression, or manual check.
- Raw external references belong in `references/`; distilled project interpretation belongs in `docs/references/`.

## Project-Specific Guardrails

Fill after applying the scaffold:

- `PROJECT_PLACEHOLDER(dependency-rules): allowed and forbidden dependencies between source layers.`
- `PROJECT_PLACEHOLDER(generated-file-policy): generated files and whether Codex may edit them directly.`
- `PROJECT_PLACEHOLDER(changed-file-validation): commands required by changed path type.`
- `PROJECT_PLACEHOLDER(security-sensitive-changes): changes that require human review.`
- `PROJECT_PLACEHOLDER(external-service-mutations): external operations that require approval.`

## Tool Rules

- Allowed by default: repository-local reads, scoped edits, local validation commands, and artifact writes.
- Human approval required: credentials, production changes, external service mutation, destructive filesystem actions, broad Git history edits, pushes, merges, and ambiguous policy decisions.
- Prefer small mechanical checks over broad autonomous workflows.

## Git Rules

- Do not include unrelated human edits in a commit.
- Use functional commit prefixes such as `docs:`, `feat:`, `fix:`, `test:`, `build:`, `security:`, or `chore:`.
- Let humans decide when to commit, push, merge, or release unless a project-specific workflow explicitly says otherwise.

## Future Checks

Add checks only when they enforce a real project rule:

- Dependency boundary checker.
- Changed-file validation checker.
- Secret or credential scanner.
- Documentation link checker.
- UI screenshot or accessibility check.
