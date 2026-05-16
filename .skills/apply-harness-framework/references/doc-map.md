# Harness Document Map

Use this reference to decide where project-specific facts belong while applying the lightweight framework.

## Top-Level Files

- `AGENTS.md`: short repository map, agent rules, required first checks, and links to deeper docs. Keep it concise.
- `README.md`: human-facing introduction, adoption workflow, commands, and examples.
- `ARCHITECTURE.md`: project shape, source layers, dependency boundaries, extension points, state, service boundaries, and approval boundaries.
- `PLANS.md`: framework roadmap in the scaffold; project harness milestones after adoption.

## Focused Docs

- `docs/ENVIRONMENT.md`: language runtimes, package managers, dependency installation, local services, ports, environment variables, setup commands.
- `docs/RUNTIME.md`: target project runtime model, entrypoints, configuration, services, ports, state, logs, stop conditions, and packaging or deployment runtime differences.
- `docs/OBSERVABILITY.md`: logs, traces, screenshots, validation evidence, reproduction commands, and retention rules.
- `docs/GUARDRAILS.md`: architecture rules, changed-file validation requirements, safety rules, and checks that should become mechanical.
- `docs/SECURITY.md`: secret handling, credential boundaries, production restrictions, external system mutations, and security review triggers.
- `docs/EVALUATION.md`: validation commands, acceptance criteria, manual checks, and evidence policy.

## Support Directories

- `docs/exec-plans/active/`: current substantial work plans.
- `docs/exec-plans/completed/`: completed work plans with decisions and validation results.
- `docs/product-specs/`: controlled language, product conventions, and project-specific specs.
- `docs/references/`: distilled project-local interpretations of long-lived references.
- `references/`: raw or external source material used by agents.
- `tools/`: validators and small operational utilities.
- `artifacts/`: ignored local logs, traces, screenshots, and validation evidence.
- `.skills/`: repo-local skills that help Codex apply or operate the framework.

## Placement Rules

- Put facts where future agents will look for them during work.
- Keep `AGENTS.md` as a map, not a knowledge base.
- Put reusable project rules in docs before turning them into scripts.
- Put raw external material in `references/` and distilled project interpretation in `docs/references/`.
- Put generated or run-specific evidence under `artifacts/`.
- Prefer execution plans over a machine task queue unless the user explicitly asks for automation.
