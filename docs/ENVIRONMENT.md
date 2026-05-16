# Environment

Status: project-specific scaffold.

Define project-specific local setup here when this framework is applied to a real repository. Replace each `PROJECT_PLACEHOLDER(...)` entry with facts discovered from the target project.

## Language Runtime

- `PROJECT_PLACEHOLDER(language-runtime): required language runtimes, versions, package managers, and version managers.`

## Dependency Installation

- `PROJECT_PLACEHOLDER(dependency-install): deterministic dependency installation commands and lockfiles.`

## Local Services

- `PROJECT_PLACEHOLDER(local-services): databases, queues, browsers, emulators, containers, or background services needed for local validation.`

## Ports

- `PROJECT_PLACEHOLDER(ports): local service ports, conflict policy, and reserved ranges.`

## Environment Variables

- `PROJECT_PLACEHOLDER(environment-variables): required variables, safe defaults, secret handling, and redaction rules.`

## Reproducible Setup Command

- `PROJECT_PLACEHOLDER(setup-command): command or script that prepares a clean checkout for local validation.`

## First Safe Check

- `PROJECT_PLACEHOLDER(first-safe-check): the safest command a new agent can run to prove the environment is usable.`
