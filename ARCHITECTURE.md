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

Status: project-specific placeholder.

Fill this section when applying the framework to a real repository. Do not invent product boundaries in the generic scaffold.

Record intended dependency direction before encoding it mechanically.

Boundary placeholders:

- `TODO: identify source layers or packages, such as ui, api, domain, infrastructure, generated, or tests.`
- `TODO: list allowed imports between layers or packages.`
- `TODO: list forbidden imports between layers or packages.`
- `TODO: identify generated files and whether agents may edit them directly.`
- `TODO: identify migration, schema, or contract files that require special validation.`

Mechanical check placeholder:

- `TODO: encode dependency boundaries in tools/check_dependency_boundaries.py, an existing linter config, or CI.`

## Product-Specific Architecture Rules

Status: project-specific placeholder.

Use this section only after the framework is applied to a real product repository.

Rules to discover and fill:

- `TODO: source-of-truth files for product behavior, contracts, schemas, and generated artifacts.`
- `TODO: ownership boundaries for product modules or services.`
- `TODO: runtime services, ports, databases, queues, and external systems.`
- `TODO: build, test, lint, typecheck, migration, and UI verification commands required by changed paths.`
- `TODO: deployment, production mutation, credential, and approval boundaries.`

## Open Decisions

- Runtime language:
- State backend:
- Tool permission model:
- Eval runner:
- Observability backend:
