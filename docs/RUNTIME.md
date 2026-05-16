# Runtime

Status: lightweight scaffold.

This document records how the target project runs. It should describe product or application runtime behavior, not the human/Codex collaboration process.

Fill project-specific commands and runtime facts after the scaffold is applied to a real codebase.

## Runtime Model

- `PROJECT_PLACEHOLDER(runtime-model): describe whether the project runs as a web app, CLI, desktop app, service, worker, library, package, scheduled job, or another runtime shape.`
- `PROJECT_PLACEHOLDER(process-model): describe long-running processes, background workers, service managers, task schedulers, or user-session requirements.`
- `PROJECT_PLACEHOLDER(startup-order): list startup order for apps, services, databases, queues, browsers, or emulators.`

## Entrypoints

Fill only commands discovered from repository files or safe command output.

- Development: `PROJECT_PLACEHOLDER(dev-command): local development server, app, CLI, or worker command.`
- Production-like run: `PROJECT_PLACEHOLDER(run-command): command that starts the project in its normal runtime mode.`
- Debug run: `PROJECT_PLACEHOLDER(debug-command): useful local reproduction or verbose logging command.`
- One-shot or maintenance command: `PROJECT_PLACEHOLDER(one-shot-command): migrations, jobs, scripts, packaging, or administrative commands.`

## Configuration

- `PROJECT_PLACEHOLDER(config-files): runtime config files, search order, and defaults.`
- `PROJECT_PLACEHOLDER(environment-variables): environment variables used at runtime, with safe defaults and secret handling.`
- `PROJECT_PLACEHOLDER(feature-flags): feature flags, modes, profiles, or environment names.`
- `PROJECT_PLACEHOLDER(config-reload): whether config changes require restart, reload, rebuild, or redeploy.`

## Local Services And Ports

- `PROJECT_PLACEHOLDER(local-services): databases, queues, browsers, emulators, containers, or background services required at runtime.`
- `PROJECT_PLACEHOLDER(ports): local ports, conflict policy, hostnames, and health endpoints.`
- `PROJECT_PLACEHOLDER(service-health): commands or URLs that prove services are ready.`

## Runtime State

- `PROJECT_PLACEHOLDER(runtime-state): local databases, caches, queues, generated files, browser storage, or service state.`
- `PROJECT_PLACEHOLDER(state-location): filesystem paths, database names, buckets, queues, or external stores.`
- `PROJECT_PLACEHOLDER(state-reset): safe local reset commands and data-loss warnings.`

## Logs And Diagnostics

- `PROJECT_PLACEHOLDER(log-locations): local app, service, worker, browser, or package logs.`
- `PROJECT_PLACEHOLDER(log-levels): supported log levels and how to enable verbose diagnostics.`
- `PROJECT_PLACEHOLDER(diagnostic-commands): commands that inspect status, health, state, queues, or background jobs.`

Detailed evidence and retention rules live in `docs/OBSERVABILITY.md`.

## Failure And Stop Conditions

- `PROJECT_PLACEHOLDER(normal-stop): how to stop the app or service cleanly.`
- `PROJECT_PLACEHOLDER(restart-behavior): when restart is required and how state survives restart.`
- `PROJECT_PLACEHOLDER(recoverable-failures): failures the project can log and continue after.`
- `PROJECT_PLACEHOLDER(unrecoverable-failures): failures that should stop startup or require human action.`
- `PROJECT_PLACEHOLDER(timeout-policy): request, job, worker, or startup timeout expectations.`

## Deployment Or Packaging Runtime

Fill only when the target project has deployable or packaged runtime behavior:

- `PROJECT_PLACEHOLDER(build-output): generated runtime package, executable, container, or artifact locations.`
- `PROJECT_PLACEHOLDER(deploy-runtime): production, staging, desktop, mobile, or package runtime differences.`
- `PROJECT_PLACEHOLDER(rollback-or-uninstall): rollback, uninstall, downgrade, or cleanup behavior.`
