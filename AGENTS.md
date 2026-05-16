# Lightweight Codex Harness

This repository is a universal starting point for a small, human-in-the-loop Codex harness. Treat it as project working structure, not as an autonomous task platform.

## Repository Map

- `ARCHITECTURE.md`: project shape, boundaries, extension points, state, and open decisions.
- `PLANS.md`: roadmap and current milestones.
- `docs/ENVIRONMENT.md`: setup, dependencies, services, ports, and environment variables.
- `docs/RUNTIME.md`: how the target project runs: entrypoints, configuration, services, state, and stop conditions.
- `docs/EVALUATION.md`: validation commands, manual checks, and acceptance evidence.
- `docs/GUARDRAILS.md`: project rules and checks worth preserving.
- `docs/OBSERVABILITY.md`: logs, screenshots, traces, and local evidence locations.
- `docs/SECURITY.md`: secrets, credentials, external systems, and approval boundaries.
- `docs/exec-plans/`: active and completed plans for substantial work.
- `references/`: external or raw long-lived source material; use `docs/references/` for project-local interpretation.
- `.skills/`: repo-local Codex skills for applying and operating the harness.
- `tools/`: small mechanical checks and operational utilities.
- `artifacts/`: ignored local logs, screenshots, traces, and validation evidence when they explain a decision.

## Agent Rules

- Prefer repository-local knowledge over unstated assumptions.
- Keep this file short; add durable detail to focused docs and link it here.
- Let humans own goals, judgment calls, credentials, production changes, and destructive actions.
- Use Codex for scoped implementation, documentation updates, validation, and evidence capture.
- Convert important repeated rules into scripts, lint checks, CI checks, or structural tests when feasible.
- Record substantial work in `docs/exec-plans/active/` while it is in progress, then move it to `docs/exec-plans/completed/`.
- Preserve logs, traces, screenshots, and validation output only when they explain a decision or regression.
- Use functional Git commit prefixes such as `docs:`, `feat:`, `fix:`, `test:`, `build:`, `security:`, or `chore:`.
- Escalate to a human for credentials, production changes, destructive actions, ambiguous policy decisions, and any operation outside the harness permission model.

## Required First Check

Run the structural validator after changing the framework layout or core docs:

```bash
python tools/validate_harness_structure.py
```
