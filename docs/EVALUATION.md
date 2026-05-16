# Evaluation

Status: lightweight scaffold.

This document records validation commands, acceptance criteria, and manual checks. It does not assume a generic eval runner.

## Structural Validation

Run after changing the harness layout or core docs:

```bash
python tools/validate_harness_structure.py
```

## Project Validation Commands

Fill after applying the scaffold:

- Setup check: `PROJECT_PLACEHOLDER(setup-check): command that proves dependencies and local setup are usable.`
- Unit tests: `PROJECT_PLACEHOLDER(unit-tests): command for the normal unit test suite.`
- Integration tests: `PROJECT_PLACEHOLDER(integration-tests): command and required local services.`
- Lint/typecheck: `PROJECT_PLACEHOLDER(lint-typecheck): command for linting, formatting, or type checks.`
- Build/package: `PROJECT_PLACEHOLDER(build-package): command for production build, package, or executable generation.`
- UI/manual check: `PROJECT_PLACEHOLDER(ui-manual-check): browser, viewport, screenshot, or manual verification steps.`

Only document commands that are discovered from repository files or safe command output.

## Acceptance Evidence

Keep evidence under `artifacts/` only when it explains a decision, regression, or manual check.

Useful evidence examples:

- A failing command output that guided the fix.
- A before/after screenshot for a UI change.
- A small trace or log excerpt that proves a runtime behavior.
- A package or executable validation note.

Avoid preserving noisy logs, secrets, credentials, private user data, or screenshots with sensitive content.

## Before Finishing Work

For a normal Codex task:

1. Run the most relevant validation command available.
2. Run `python tools/validate_harness_structure.py` if the harness layout changed.
3. Record unrun checks and the reason in the final response.
4. Move active execution plans to completed when substantial work is done.

## Future Automation

Project-specific eval suites can be added later if a repeated workflow needs them. Add the smallest useful script or CI job first, then document it here.
