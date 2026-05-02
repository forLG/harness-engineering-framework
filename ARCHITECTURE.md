# Architecture

This document defines the universal harness architecture. Project-specific facts use `PROJECT_PLACEHOLDER(...)` until the framework is applied to a real repository.

## Runtime Core

Status: implemented.

The runtime should provide:

- Task intake and normalization.
- Tool execution with explicit permissions.
- File-based state persistence for task progress, decisions, and artifacts.
- Stop conditions, retry rules, and failure classification.
- Isolated execution environments for local runs, tests, and UI verification.

## Extension Points

Status: implemented.

Expected extension points:

- Tool adapters.
- Repository knowledge indexers.
- Evaluation runners.
- Observability collectors.
- Policy and guardrail checks.
- Reviewer or maintenance agents.

## State Model

Status: implemented.

Define where these records live:

- Task request: `runtime/tasks/queue/*.json`.
- Plan and progress: `docs/exec-plans/active/`, task status directories under `runtime/tasks/`, and `artifacts/runs/<run-id>/summary.json`.
- Tool calls and outputs: role outputs under `artifacts/runs/<run-id>/`.
- Artifacts: `artifacts/`.
- Eval results: `evals/results/`.
- Human approvals and escalation history: task status, role JSON output, and preserved run artifacts.

## Isolation Model

Status: scaffold.

Define how the harness separates:

- Worktrees or task branches: current scaffold runs in the active repository; target projects may add task branches or worktrees.
- Local services and ports: `PROJECT_PLACEHOLDER(local-services): document services, ports, and startup order for the target project.`
- Credentials and secrets: `PROJECT_PLACEHOLDER(credentials): document secret sources, redaction rules, and escalation boundaries for the target project.`
- Runtime artifacts: stored under `artifacts/`.
- Production or external systems: `PROJECT_PLACEHOLDER(external-systems): document production, staging, and external mutation boundaries for the target project.`

## Dependency Boundaries

Status: project-specific.

Fill this section when applying the framework to a real repository. Do not invent product boundaries in the generic scaffold.

Record intended dependency direction before encoding it mechanically.

Fill these placeholders:

- `PROJECT_PLACEHOLDER(source-layers): identify source layers or packages, such as ui, api, domain, infrastructure, generated, or tests.`
- `PROJECT_PLACEHOLDER(allowed-imports): list allowed imports between layers or packages.`
- `PROJECT_PLACEHOLDER(forbidden-imports): list forbidden imports between layers or packages.`
- `PROJECT_PLACEHOLDER(generated-files): identify generated files and whether agents may edit them directly.`
- `PROJECT_PLACEHOLDER(contract-files): identify migration, schema, or contract files that require special validation.`

Mechanical check:

- `PROJECT_PLACEHOLDER(dependency-boundary-check): encode dependency boundaries in a repository-local checker, existing linter config, or CI.`

## Product-Specific Architecture Rules

Status: project-specific.

Use this section only after the framework is applied to a real product repository.

Rules to discover and fill:

- `PROJECT_PLACEHOLDER(source-of-truth): source-of-truth files for product behavior, contracts, schemas, and generated artifacts.`
- `PROJECT_PLACEHOLDER(ownership): ownership boundaries for product modules or services.`
- `PROJECT_PLACEHOLDER(runtime-services): runtime services, ports, databases, queues, and external systems.`
- `PROJECT_PLACEHOLDER(validation-matrix): build, test, lint, typecheck, migration, and UI verification commands required by changed paths.`
- `PROJECT_PLACEHOLDER(approval-boundaries): deployment, production mutation, credential, and approval boundaries.`

## Open Decisions

- Runtime language: Python supervisor scripts plus Codex CLI role invocations.
- State backend: repository-local JSON, Markdown, and artifact files.
- Tool permission model: Codex sandboxing plus role-level escalation rules.
- Eval runner: `tools/run_evals.py`.
- Observability backend: repository-local artifacts under `artifacts/`.
