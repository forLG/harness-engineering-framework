# Observability

Status: lightweight scaffold.

This document defines where to keep logs, screenshots, traces, and validation evidence that are useful to future humans or agents.

## Evidence Policy

Preserve evidence when it explains:

- A decision.
- A regression.
- A manual validation result.
- A failure that future work may need to reproduce.
- A security, privacy, or reliability judgment.

Do not preserve evidence just because a command produced output. Keep artifacts small, reviewed, and free of secrets or sensitive personal data.

## Repository Evidence

- `artifacts/`: ignored local evidence root.
- `artifacts/test-*`: suggested prefix for local test output.
- `artifacts/screenshots/`: optional UI screenshots when a task needs visual proof.
- `artifacts/logs/`: optional logs worth keeping beyond the local command.
- `artifacts/traces/`: optional traces or timelines worth keeping.

Create subdirectories as needed for the project. Keep a short note with any artifact whose purpose is not obvious.

## Project Observability

Fill after applying the scaffold:

- `PROJECT_PLACEHOLDER(log-format): log format, minimum fields, and redaction rules.`
- `PROJECT_PLACEHOLDER(log-locations): local and deployed log locations.`
- `PROJECT_PLACEHOLDER(trace-format): trace format, timeline schema, and correlation identifiers.`
- `PROJECT_PLACEHOLDER(screenshot-policy): screenshot, video, or UI artifact capture policy.`
- `PROJECT_PLACEHOLDER(reproduction-data): seed data, fixtures, or commands needed to replay important failures.`

## Retention

- Keep evidence only as long as it remains useful.
- Do not commit secrets, credentials, private user data, or sensitive screenshots.
- Prefer summaries in completed execution plans over large raw outputs.
