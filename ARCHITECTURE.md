# Architecture

This document defines the universal harness architecture. Fill project-specific choices when the framework is applied to a real repository.

## Runtime Core

Status: placeholder.

The runtime should provide:

- Task intake and normalization.
- Tool execution with explicit permissions.
- State persistence for task progress, decisions, and artifacts.
- Stop conditions, retry rules, and failure classification.
- Isolated execution environments for local runs, tests, and UI verification.

## Extension Points

Status: placeholder.

Expected extension points:

- Tool adapters.
- Repository knowledge indexers.
- Evaluation runners.
- Observability collectors.
- Policy and guardrail checks.
- Reviewer or maintenance agents.

## State Model

Status: placeholder.

Define where these records live:

- Task request.
- Plan and progress.
- Tool calls and outputs.
- Artifacts.
- Eval results.
- Human approvals and escalation history.

## Isolation Model

Status: placeholder.

Define how the harness separates:

- Worktrees or task branches.
- Local services and ports.
- Credentials and secrets.
- Runtime artifacts.
- Production or external systems.

## Dependency Boundaries

Status: placeholder.

Encode final boundaries as mechanical checks. Until then, record intended dependency direction here.

## Open Decisions

- Runtime language:
- State backend:
- Tool permission model:
- Eval runner:
- Observability backend:
