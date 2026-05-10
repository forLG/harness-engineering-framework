# Artifacts

Status: project-specific.

This directory is the repository-local bucket for temporary test output,
debugging evidence, and manually reviewed validation evidence.

Use `artifacts/` when a command needs a writable path inside the repository,
especially in sandboxed agent runs where OS temp directories may be restricted.

## Allowed Local Output

- `artifacts/test-logs/`: logs created by tests.
- `artifacts/test-localappdata/`: fake `%LOCALAPPDATA%` trees used by tests.
- `artifacts/test-screenshots/`: screenshot retention and capture test output.
- `artifacts/test-state/`: deduplication and config state files created by tests.
- `artifacts/logs/`: preserved redacted logs when they explain a decision or regression.

## Rules

- Do not place temporary test output in the repository root.
- Do not commit generated files under `artifacts/` unless a human explicitly wants the redacted evidence preserved.
- Do not store credentials, raw QR payloads, or unreviewed screenshots here.
- Prefer deterministic test fixtures under `tests/fixtures/`; use `artifacts/` only for generated output.
- Real product runs should still use `%LOCALAPPDATA%\QRWatch\` by default, not this directory.
