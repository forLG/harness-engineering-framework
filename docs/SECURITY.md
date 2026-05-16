# Security

Status: lightweight scaffold.

This document records secrets, credentials, privacy rules, and operations that require human approval.

## Default Rules

- Never commit credentials, tokens, private keys, session cookies, provider passwords, or webhook URLs.
- Treat `.env`, `.env.*`, local config files, screenshots, traces, and logs as potentially sensitive.
- Redact secrets in docs, artifacts, final responses, and issue or PR comments.
- Use test accounts, dry-run modes, or local mocks before real external sends or mutations.
- Escalate to a human for production changes, credential setup, destructive operations, or ambiguous policy decisions.

## Project-Specific Secret Sources

Fill after applying the scaffold:

- `PROJECT_PLACEHOLDER(secret-files): ignored local files that may contain secrets.`
- `PROJECT_PLACEHOLDER(secret-stores): password managers, CI secret stores, cloud secret managers, or local OS stores.`
- `PROJECT_PLACEHOLDER(required-credentials): credentials required for local development or validation.`
- `PROJECT_PLACEHOLDER(redaction-rules): values that must be redacted from logs and artifacts.`

## External Systems

Fill after applying the scaffold:

- `PROJECT_PLACEHOLDER(external-systems): APIs, providers, production services, billing systems, notification channels, or cloud resources.`
- `PROJECT_PLACEHOLDER(safe-test-targets): test recipients, sandboxes, staging endpoints, or local mocks.`
- `PROJECT_PLACEHOLDER(mutation-approval): operations that require explicit human approval.`

## Security Review Triggers

Require human review for:

- Authentication, authorization, session, or permission changes.
- Secrets, credential loading, or logging changes.
- Payment, billing, notification, or external provider mutation.
- Production deployment or migration behavior.
- Storage of raw user data, screenshots, payloads, or personal information.

## Current Scaffold Notes

The generic framework has no required credentials and no networked runtime. Any real secret rules must come from the target project.
