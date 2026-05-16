# Lightweight Codex Harness

This repository is a small starting point for using Codex in a real software project.

The harness is intentionally human-in-the-loop. A human chooses the work, keeps product judgment, reviews results, and decides what should become durable structure. Codex helps inspect the repository, implement changes, update docs, run checks, and preserve useful evidence.

This is not an autonomous task platform. The default loop is simple:

1. Describe the task in the chat or in `docs/exec-plans/active/`.
2. Let Codex inspect the repository and make a scoped change.
3. Run project validation commands.
4. Move useful plans or notes into `docs/exec-plans/completed/`.
5. Keep only evidence that explains a decision, regression, or manual check.

## What This Framework Provides

- `AGENTS.md`: short instructions and repository map for future Codex runs.
- `ARCHITECTURE.md`: project shape, boundaries, state, extension points, and open decisions.
- `PLANS.md`: roadmap and milestone index.
- `docs/ENVIRONMENT.md`: local setup, dependencies, services, ports, and environment variables.
- `docs/RUNTIME.md`: how the target project runs: entrypoints, configuration, services, state, and stop conditions.
- `docs/EVALUATION.md`: validation commands, manual checks, and acceptance evidence.
- `docs/GUARDRAILS.md`: project rules that should be preserved or turned into checks.
- `docs/OBSERVABILITY.md`: logs, screenshots, traces, and evidence locations.
- `docs/SECURITY.md`: secrets, credentials, external systems, and approval boundaries.
- `docs/exec-plans/`: active and completed plans for substantial work.
- `.skills/apply-harness-framework/`: a repo-local Codex skill for adapting this scaffold to a target project.
- `tools/validate_harness_structure.py`: a small structure check.
- `artifacts/`: ignored local evidence, used only when evidence is worth keeping.
- `references/`: raw or external long-lived source material.

## Apply It To A Real Project

Copy this scaffold into the target repository, then start Codex there:

```bash
codex -C path/to/project
```

Ask Codex to apply the local skill:

```text
Use .skills/apply-harness-framework/SKILL.md to apply this lightweight harness.

First inspect the repository structure, manifests, scripts, tests, CI, docs, runtime config, and existing conventions.

Fill only facts grounded in files or safe command output. Do not invent setup commands, service ports, architecture boundaries, owners, security rules, deployment rules, or validation commands.

When a fact cannot be discovered, leave PROJECT_PLACEHOLDER(<key>): <exact missing information and likely source>.

Keep AGENTS.md concise. Put durable detail in focused docs. Run python tools/validate_harness_structure.py after the framework layout changes.
```

If repo-local skills are available in your Codex environment, this shorter prompt is enough:

```text
Use $apply-harness-framework to apply this scaffold to the current repository.
```

## Adoption Passes

Use passes instead of one giant rewrite.

### 1. Orientation

Fill `AGENTS.md`, `ARCHITECTURE.md`, and `docs/ENVIRONMENT.md`.

Outcome: a future agent can understand the repository shape, setup path, and first safe validation command.

### 2. Runtime And Evidence

Fill `docs/RUNTIME.md`, `docs/OBSERVABILITY.md`, and `docs/EVALUATION.md`.

Outcome: the project runtime, validation commands, and evidence locations are clear.

### 3. Guardrails And Security

Fill `docs/GUARDRAILS.md` and `docs/SECURITY.md`.

Outcome: important project rules are explicit, and stable ones can become scripts, lint rules, tests, or CI checks.

### 4. Planning

Fill `PLANS.md` and create active execution plans only when the work is substantial.

Outcome: the project has a visible roadmap without requiring a machine task queue.

## Core Command

Validate the harness layout:

```bash
python tools/validate_harness_structure.py
```

Run normal project checks from `docs/EVALUATION.md` once the scaffold is applied to a real project.

## Operating Principle

Keep the framework small enough that a human will actually use it. Add automation only after a workflow has proven useful in real work.
