# Architecture

Status: lightweight scaffold.

This repository defines a small Codex harness that can be copied into a real project and filled from evidence. Project-specific facts use `PROJECT_PLACEHOLDER(...)` until the scaffold is applied.

## Harness Shape

The harness has four durable layers:

- Entry map: `AGENTS.md`, `README.md`, `ARCHITECTURE.md`, and `PLANS.md`.
- Focused project docs: setup, runtime, validation, guardrails, observability, and security under `docs/`.
- Working plans: active and completed execution plans under `docs/exec-plans/`.
- Mechanical checks and evidence: small scripts under `tools/` and reviewed local artifacts under `artifacts/`.

The default operating model is interactive Codex with human supervision. Automation should be added only after a project has repeated a workflow enough times to justify it.

## Project Shape

Fill this section when applying the scaffold to a real repository.

- `PROJECT_PLACEHOLDER(project-purpose): describe what the project does.`
- `PROJECT_PLACEHOLDER(primary-entrypoints): list application, CLI, service, package, or UI entrypoints.`
- `PROJECT_PLACEHOLDER(source-layout): list important source, test, config, and generated directories.`
- `PROJECT_PLACEHOLDER(runtime-model): describe how the project runs locally and in deployed environments.`

## Dependency Boundaries

Record intended dependency direction before encoding it mechanically.

- `PROJECT_PLACEHOLDER(source-layers): identify source layers or packages.`
- `PROJECT_PLACEHOLDER(allowed-imports): list allowed imports between layers or packages.`
- `PROJECT_PLACEHOLDER(forbidden-imports): list forbidden imports between layers or packages.`
- `PROJECT_PLACEHOLDER(generated-files): identify generated files and whether agents may edit them directly.`
- `PROJECT_PLACEHOLDER(contract-files): identify migration, schema, or contract files that require special validation.`

Mechanical check:

- `PROJECT_PLACEHOLDER(dependency-boundary-check): encode dependency boundaries in a repository-local checker, existing linter config, or CI when the rule is stable.`

## Extension Points

Fill with target-project facts:

- `PROJECT_PLACEHOLDER(extension-points): list plugin points, provider adapters, integrations, feature modules, or configuration surfaces.`
- `PROJECT_PLACEHOLDER(non-extension-points): list code paths that should stay closed or require human review before extension.`

## State And Artifacts

Fill with target-project facts:

- `PROJECT_PLACEHOLDER(runtime-state): local files, databases, caches, queues, or browser storage used by the product.`
- `PROJECT_PLACEHOLDER(generated-output): generated build, package, or report output locations.`
- `PROJECT_PLACEHOLDER(evidence-artifacts): logs, traces, screenshots, or validation outputs worth preserving under artifacts.`

Repository `artifacts/` is for reviewed local evidence only. It should not become the default product runtime store.

## Isolation And Approval Boundaries

Fill with target-project facts:

- `PROJECT_PLACEHOLDER(local-services): services, ports, containers, emulators, or background jobs needed locally.`
- `PROJECT_PLACEHOLDER(credentials): secret sources, redaction rules, and credential owners.`
- `PROJECT_PLACEHOLDER(external-systems): APIs, providers, production systems, or mutable external resources.`
- `PROJECT_PLACEHOLDER(approval-boundaries): changes or commands that require human approval.`

## Open Decisions

- Keep the scaffold human-supervised by default.
- Add task queues, role agents, eval runners, or autonomous loops only as project-specific extensions after a real workflow proves they are useful.
