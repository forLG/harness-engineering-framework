# Simplify Main Harness

Status: completed.

Goal: reshape the generic `main` harness so it matches the lighter human-in-the-loop approach that worked in the `qrwatch` branch.

## Completed Changes

- Rewrote `README.md`, `AGENTS.md`, `ARCHITECTURE.md`, and `PLANS.md` around a lightweight human-supervised workflow.
- Replaced the core docs with focused scaffold versions for environment, runtime, evaluation, guardrails, observability, and security.
- Removed the automatic task-loop, role-agent, eval runner, entropy runner, and runtime queue scaffolding from the framework.
- Updated `.skills/apply-harness-framework/` so future applications use the lighter adoption workflow.
- Simplified `tools/validate_harness_structure.py` to validate the lightweight structure and reject retired heavy scaffold paths.
- Added `artifacts/README.md` as the evidence policy entry point.

## Validation

```bash
python tools/validate_harness_structure.py
```

Result: passed.
