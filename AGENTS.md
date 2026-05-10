# QR Watch Harness

This repository is a lightweight Codex harness for a Windows Python background app. The app periodically screenshots the logged-in desktop, detects QR codes, and notifies a configured channel through a provider interface such as email, QQ Mail, WeChat, or webhook.

## Repository Map

- `ARCHITECTURE.md`: app architecture, source layers, privacy rules, and extension points.
- `PLANS.md`: planning index and current roadmap.
- `docs/ENVIRONMENT.md`: Windows and Python setup assumptions, dependencies, and environment variables.
- `environment.yml`: Conda environment definition for the `qrwatch` Python runtime.
- `docs/RUNTIME.md`: QR Watch product run modes, entrypoints, state, and stop conditions.
- `docs/EVALUATION.md`: test commands, validation expectations, manual checks, and acceptance evidence.
- `docs/GUARDRAILS.md`: rules agents and code changes should preserve, with mechanical checks where feasible.
- `docs/OBSERVABILITY.md`: logs, screenshots, counters, and local evidence locations.
- `docs/PACKAGING.md`: Windows executable build and package validation.
- `docs/product-specs/`: product-specific preferences and conventions.
- `docs/exec-plans/`: active and completed plans for substantial agent-assisted tasks.
- `references/`: external or raw long-lived source material used by agents; use `docs/references/` for project-local interpretation.
- `.skills/`: repo-local Codex skills for applying and operating the harness.
- `tools/`: mechanical checks and operational utilities.
- `artifacts/`: ignored local test output and explicit reviewed validation evidence; see `artifacts/README.md`.

## Agent Rules

- Prefer repository-local knowledge over unstated assumptions.
- Keep this file short; add durable detail to focused docs and link it here.
- Treat screenshots, QR payloads, notification credentials, mailbox tokens, webhook URLs, QQ credentials, and WeChat credentials as sensitive.
- Do not preserve screenshots or QR payloads in artifacts unless a task explicitly requires evidence and sensitive content has been reviewed or redacted.
- Put generated test output under `artifacts/test-*` instead of scattering temporary files in the repository root.
- Convert stable rules into scripts, lint checks, CI checks, or structural tests when feasible.
- Record substantial work in `docs/exec-plans/active/` while it is in progress, then move it to `docs/exec-plans/completed/`.
- Preserve logs, screenshots, and test output only when they explain a decision or regression.
- Use functional Git commit prefixes such as `docs:`, `feat:`, `fix:`, `test:`, `build:`, `security:`, or `chore:`.
- Escalate to a human for credentials, real notification account setup, production or external sends, destructive actions, ambiguous policy decisions, and any operation outside the harness permission model.

## Required First Check

Run the structural validator after changing the framework layout or core docs:

```bash
python tools/validate_harness_structure.py
```
