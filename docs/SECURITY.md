# Security

Status: scaffold.

Define the harness security model before connecting production systems or sensitive repositories.

## Secrets

- Storage: `PROJECT_PLACEHOLDER(secret-storage): name approved secret stores, local env files, and files that must never contain secrets.`
- Access: `PROJECT_PLACEHOLDER(secret-access): define who or what may access secrets and which tasks require human approval.`
- Rotation: `PROJECT_PLACEHOLDER(secret-rotation): define rotation ownership and escalation steps after exposure.`
- Redaction: `PROJECT_PLACEHOLDER(secret-redaction): define log, trace, screenshot, and artifact redaction requirements.`

## Permissions

- Default tool permissions: local repository reads, edits, validation commands, and artifact writes.
- Escalation process: stop the task and record a blocked result when credentials, production access, destructive actions, dirty auto-commit preflight, Git identity setup, or unclear policy choices are required.
- Disallowed operations: automatic pushes, production writes, credential access without approval, destructive filesystem actions without approval.

## Git Automation

The Ralph loop may create local commits only when auto-commit is explicitly enabled and the worktree is clean before the run starts. The loop must not push, merge, tag, or rewrite history without human approval.

## Data Handling

- Sensitive files: `PROJECT_PLACEHOLDER(sensitive-files): list source paths, config files, data exports, and generated artifacts that require special handling.`
- External uploads: `PROJECT_PLACEHOLDER(external-uploads): define whether agents may upload artifacts, logs, screenshots, or source snippets outside the repository.`
- Logs and traces: `PROJECT_PLACEHOLDER(log-trace-data): define data classes that must be redacted or excluded from preserved evidence.`

## Human Escalation

Require human approval for credentials, destructive operations, production writes, and unclear policy decisions.
