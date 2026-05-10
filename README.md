# QR Watch Harness

This repository contains QR Watch, a Windows Python background app with a
lightweight Codex harness around it.

QR Watch periodically screenshots the logged-in desktop, detects QR codes, and
notifies a configured channel through a provider interface such as dry-run logs,
QQ Mail-compatible SMTP email, webhook, QQ, or WeChat.

The harness is intentionally human-driven: a human asks an agent for help in the
CLI or editor extension, and the repository provides enough structure for the
agent to understand the project, make scoped changes, and run the right checks.
There is no automatic task queue, role runner, or cleanup loop.

## Current App Shape

Implemented source lives under `src/qrwatch/` and includes:

- configuration loading from local dotenv-style files and `QRWATCH_*` variables.
- one-shot capture, background run, dry-run, and tray entrypoints.
- mss-backed screenshot capture.
- OpenCV-backed QR detection.
- event shaping and deduplication state.
- dry-run and QQ Mail-compatible SMTP notification dispatch.
- local logging, optional screenshot retention, and PyInstaller packaging.

## Core Commands

Validate the lightweight harness structure:

```bash
python tools/validate_harness_structure.py
```

Run the product tests:

```bash
conda run -n qrwatch python -m pytest
```

Run the environment import smoke test:

```bash
conda run -n qrwatch python -c "import cv2, mss, PIL, numpy, dotenv, requests, pytest, pystray; print('python ok'); print(cv2.__version__)"
```

Start QR Watch in dry-run mode:

```bash
conda run -n qrwatch python -m qrwatch
```

Run one capture/detect/notify cycle without external sends:

```bash
conda run -n qrwatch python -m qrwatch --once --dry-run
```

Start the tray app:

```bash
conda run -n qrwatch python -m qrwatch --tray
```

Build the Windows executable:

```powershell
.\tools\build_windows_executable.ps1
```

See `docs/EVALUATION.md` for the full testing and manual validation matrix.

## Repository Map

- `AGENTS.md`: short agent entrypoint, sensitive-data rules, and required checks.
- `ARCHITECTURE.md`: product architecture, source layers, boundaries, state model, and extension points.
- `PLANS.md`: QR Watch roadmap and milestone history.
- `docs/ENVIRONMENT.md`: Windows, Python, Conda, dependencies, and environment variables.
- `docs/RUNTIME.md`: product run modes, entrypoints, runtime state, privacy defaults, and stop conditions.
- `docs/EVALUATION.md`: test commands, reproduction commands, manual checks, and acceptance evidence.
- `docs/OBSERVABILITY.md`: log, screenshot, counter, and evidence locations.
- `docs/GUARDRAILS.md`: structural, dependency, safety, tool, and Git guardrails.
- `docs/SECURITY.md`: secrets, screenshots, QR payloads, external sends, and human escalation.
- `docs/PACKAGING.md`: PyInstaller build path and executable validation.
- `docs/product-specs/`: project-specific conventions and personal preferences.
- `docs/exec-plans/`: active and completed execution plans for substantial work.
- `.skills/apply-harness-framework/`: repo-local skill for adapting the harness scaffold.
- `tools/`: mechanical validation and packaging utilities.
- `artifacts/`: ignored local test output and explicit reviewed validation evidence.
- `references/`: external or raw long-lived source material.

## Harness Principle

Keep the agent entry point short. Put durable knowledge in focused docs. Put
test and reproduction commands in `docs/EVALUATION.md`. Convert repeated rules
into scripts or tests when the rule matters enough. Preserve evidence only when
it explains a decision or regression. Put generated test output under
`artifacts/test-*`, not in the repository root, and never commit credentials,
screenshots, raw QR payloads, or generated packaging output.
