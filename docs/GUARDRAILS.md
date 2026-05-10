# Guardrails

Status: applied.

Guardrails are rules that agents and humans should preserve while changing QR
Watch. When a rule can be checked mechanically, prefer a script, lint rule, or
test over prose.

## Structural Rules

- Required files and directories are checked by `tools/validate_harness_structure.py`.
- `AGENTS.md` must stay concise and point to focused docs instead of repeating them.
- Product roadmap belongs in `PLANS.md`.
- Product architecture and source boundaries belong in `ARCHITECTURE.md`.
- Test and reproduction commands belong in `docs/EVALUATION.md`.
- Runtime logs and evidence locations belong in `docs/OBSERVABILITY.md`.
- Active execution plans belong in `docs/exec-plans/active/`; completed plans belong in `docs/exec-plans/completed/`.
- Product-specific preferences and conventions belong in `docs/product-specs/`.

## Product Dependency Guardrails

Expected source layers are documented in `ARCHITECTURE.md`.

Allowed dependencies:

- `app` may compose all product layers.
- `capture` may depend on screenshot and image libraries.
- `detectors` may depend on image and QR detection libraries.
- `notifiers` may depend on provider clients, `requests`, and standard mail libraries.
- `state` may depend on local filesystem, JSON, SQLite, hashing, and time utilities.

Forbidden dependencies:

- `detectors` must not send notifications.
- `capture` must not decode QR codes or call notifiers.
- `notifiers` must not capture screenshots.
- `tools/` should not import product runtime modules unless a specific validation command requires it.

## Product Safety Guardrails

- Do not commit notification credentials, mailbox passwords, QQ credentials, WeChat credentials, webhook URLs, provider cookies, or `.env` files.
- Do not perform real external sends unless the user explicitly provides credentials and a test recipient for that run.
- Default notifier mode must be dry-run until a real provider is configured.
- QR payloads should be hashed or redacted in persistent state and logs by default.
- Screenshots may be stored locally under `%LOCALAPPDATA%\QRWatch\screenshots\` with retention, but must not be committed.
- Repository `artifacts/` may contain logs or screenshots only when a task explicitly requires evidence and the user has reviewed or approved sensitive content.
- Generated test output belongs under `artifacts/test-*`, not in the repository root.
- Logs must redact secrets, tokens, webhook URLs, and raw QR payloads unless a debug setting explicitly allows payload logging.
- Generated packaging output must be documented before agents edit or delete it.

## Tool Rules

- Allowed tools: repository-local reads, edits, local validation commands, Conda environment checks, and artifact writes.
- Restricted tools: production changes, credential access, destructive filesystem operations, external service mutation, automatic pushes, automatic merges, tags, and history rewrites.
- Escalation-required tools: anything outside the local harness permission model or requiring secrets, real external sends, destructive actions, or ambiguous privacy decisions.

## Git Rules

- Use functional commit prefixes such as `docs:`, `feat:`, `fix:`, `test:`, `build:`, `security:`, or `chore:`.
- Commit messages should describe the function of the change, not only the files touched.
- Do not commit credentials, screenshots, raw QR payloads, runtime logs, or generated packaging output.
- Pushing, merging, tagging, and history rewriting require explicit human approval.

## Future Checks

- `tools/validate_qrwatch_boundaries.py`: dependency boundary check.
- `tools/validate_qrwatch_security.py`: secret, screenshot artifact, and unsafe notifier config check.
- Product smoke tests for capture, detection fixtures, deduplication, dry-run notifier behavior, and retention cleanup.
