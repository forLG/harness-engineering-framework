# Environment

Status: project-specific.

Define project-specific local setup here when this framework is applied to a real repository. Replace each `PROJECT_PLACEHOLDER(...)` entry with facts discovered from the target project.

## Language Runtime

- `PROJECT_PLACEHOLDER(language-runtime): list required language runtimes, versions, package managers, and version managers.`

## Dependency Installation

- `PROJECT_PLACEHOLDER(dependency-install): list deterministic dependency installation commands and lockfiles.`

## Local Services

- `PROJECT_PLACEHOLDER(local-services): list databases, queues, browsers, emulators, containers, or background services needed for local validation.`

## Ports

- `PROJECT_PLACEHOLDER(ports): list local service ports, conflict policy, and any reserved ranges.`

## Environment Variables

- `PROJECT_PLACEHOLDER(environment-variables): list required variables, safe defaults, secret handling, and redaction rules.`

## Reproducible Setup Command

- `PROJECT_PLACEHOLDER(setup-command): provide the command or script that prepares a clean checkout for local validation.`
