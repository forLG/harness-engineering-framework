# Reliability

Status: scaffold.

Define reliability expectations for the harness runtime and agent workflows.

## Failure Classes

- User input ambiguity: ask for clarification or mark the task blocked when a safe assumption is not possible.
- Tool failure: preserve command output in the run artifact and create follow-up work when retrying would hide the original failure.
- Environment failure: `PROJECT_PLACEHOLDER(environment-failure): define how to classify missing dependencies, broken local services, and machine-specific setup failures.`
- Test failure: preserve failing commands and relevant output; distinguish product failures from harness failures.
- External service failure: `PROJECT_PLACEHOLDER(external-service-failure): define retry, skip, and escalation policy for target-project services.`
- Policy or permission failure: stop and record human escalation.

## Retry Policy

- `PROJECT_PLACEHOLDER(retry-policy): define which operations may be retried, maximum attempts, timeout behavior, and evidence required after each failed attempt.`

## Rollback Policy

- `PROJECT_PLACEHOLDER(rollback-policy): define how to revert or contain failed changes, migrations, generated files, local data, and service mutations.`

## Required Evidence

Define what logs, traces, screenshots, test outputs, or eval results must be preserved for substantial changes.

- `PROJECT_PLACEHOLDER(required-evidence): list evidence required for UI, API, data, migration, security, and infrastructure changes.`
