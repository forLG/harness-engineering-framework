# Runtime

Status: placeholder.

Define how the harness invokes and supervises Codex when this framework is applied to a real project.

## Invocation Modes

Status: placeholder.

Define supported modes, such as:

- Human-supervised interactive runs.
- Non-interactive task runs.
- CI, scheduler, or issue-triggered runs.
- Review or maintenance runs.

## Runner Entrypoints

Status: placeholder.

Define the scripts, commands, or services that start harness runs.

## Task Loop

Status: placeholder.

Define the run sequence:

- Load repository context.
- Load task input.
- Create or update execution plan.
- Invoke agent.
- Capture logs, traces, artifacts, and final output.
- Run validation checks.
- Store results.
- Escalate when required.

## Human Interaction

Status: placeholder.

Define where humans can supervise, approve, interrupt, redirect, or resume runs.

## State and Artifacts

Status: placeholder.

Define where runtime state and outputs are stored, including logs, traces, screenshots, plans, diffs, and eval results.

## Stop Conditions

Status: placeholder.

Define success, failure, timeout, escalation, and retry behavior.

## Open Decisions

- Codex invocation method:
- Interactive command:
- Non-interactive command:
- Approval policy:
- JSON or trace format:
- Resume strategy:
