# Security

Status: placeholder.

Define the harness security model before connecting production systems or sensitive repositories.

## Secrets

- Storage:
- Access:
- Rotation:
- Redaction:

## Permissions

- Default tool permissions: local repository reads, edits, validation commands, and artifact writes.
- Escalation process: stop the task and record a blocked result when credentials, production access, destructive actions, dirty auto-commit preflight, Git identity setup, or unclear policy choices are required.
- Disallowed operations: automatic pushes, production writes, credential access without approval, destructive filesystem actions without approval.

## Git Automation

The Ralph loop may create local commits only when auto-commit is explicitly enabled and the worktree is clean before the run starts. The loop must not push, merge, tag, or rewrite history without human approval.

## Data Handling

- Sensitive files:
- External uploads:
- Logs and traces:

## Human Escalation

Require human approval for credentials, destructive operations, production writes, and unclear policy decisions.
