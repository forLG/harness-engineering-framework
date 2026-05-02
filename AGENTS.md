# Harness Engineering Framework

This repository is a universal starting point for a Codex-based harness. Treat it as agent infrastructure, not as a prompt bundle.

## Repository Map

- `ARCHITECTURE.md`: runtime boundaries, extension points, and system shape.
- `PLANS.md`: planning index and current roadmap.
- `docs/RUNTIME.md`: agent invocation, task loop, interaction mode, and run artifact model.
- `docs/`: durable project knowledge, quality docs, design notes, environment information, distilled references, and execution plans.
- `docs/agent-roles/`: role prompts for implementer, validator, reviewer, and follow-up planner runs.
- `references/`: external or raw long-lived source material used by agents; use `docs/references/` for project-local interpretation.
- `.skills/`: repo-local Codex skills for applying and operating the harness.
- `runtime/`: harness runtime state, task queue, and implementation placeholder.
- `tools/`: mechanical checks and operational utilities.
- `evals/`: benchmark tasks, acceptance criteria, and eval results.
- `artifacts/`: local logs, traces, screenshots, and run outputs.

## Agent Rules

- Prefer repository-local knowledge over unstated assumptions.
- Keep this file short; add durable detail to focused docs and link it here.
- Convert important rules into scripts, lint checks, CI checks, or structural tests when feasible.
- Record substantial work in `docs/exec-plans/active/` while it is in progress, then move it to `docs/exec-plans/completed/`.
- Preserve logs, traces, screenshots, and eval outputs when they explain a decision or regression.
- Treat `runtime/tasks/` as the source of truth for the outer task loop.
- Use functional Git commit prefixes such as `docs:`, `feat:`, `fix:`, `test:`, or `chore:`; see `docs/OPERATIONS.md` for the full commit message policy.
- Escalate to a human for credentials, production changes, destructive actions, ambiguous policy decisions, and any operation outside the harness permission model.

## Required First Check

Run the structural validator after changing the framework layout:

```bash
python tools/validate_harness_structure.py
```
