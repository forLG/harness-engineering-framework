# Environment

Status: applied.

This repository is being adapted for a Windows background Python app that periodically screenshots the active desktop, detects QR codes, and sends a notification through a pluggable channel such as email, QQ, WeChat, or another provider.

The app source skeleton now exists under `src/qrwatch/`. Environment facts below were established on 2026-05-09 by creating the `qrwatch` Conda environment and installing the starter package set.

## Platform

- Primary OS: Windows.
- Runtime mode: background desktop process. The first implementation should run in the logged-in user session, because Windows services do not automatically have access to the interactive desktop for screenshots.
- Packaging target: TODO: decide whether the first distributable is a plain Python script, scheduled task, tray app, Windows service wrapper, or PyInstaller executable.

## Language Runtime

- Language: Python.
- Supported Python version: Python 3.11. The created Conda environment currently resolves to Python 3.11.15.
- Package manager: Conda environment plus `pip` packages recorded in `environment.yml`.
- Version manager: Conda.
- Environment name: `qrwatch`.

## Dependency Installation

- Dependency manifest: `environment.yml`.
- Installed starter packages:
  - `mss`: Windows desktop screenshot capture.
  - `opencv-python`: QR detection through OpenCV's `QRCodeDetector`.
  - `pillow` and `numpy`: image conversion and test fixtures.
  - `python-dotenv`: local environment configuration.
  - `requests`: webhook-style notification adapters.
  - `pystray`: simple Windows system tray controller UI.
  - `pytest`: test runner.

Create the environment from the repository manifest:

```bash
conda env create -f environment.yml
```

The environment already exists on this workstation as `qrwatch`.

## Local Services

- Required local services: none for the first local prototype.
- Optional external services:
  - SMTP mailbox provider for email notifications.
  - QQ, WeChat, or webhook bridge provider if selected.
- Service credentials: must be provided by the human through local environment variables or a local ignored config file. Do not commit credentials.

## Ports

- No local ports are reserved by the current design.
- If a webhook receiver, local health server, or tray-control HTTP endpoint is added later, document its port and conflict policy here.

## Environment Variables

No variables are required for the default dry-run startup. The current package skeleton recognizes:

- `QRWATCH_INTERVAL_SECONDS`: screenshot interval.
- `QRWATCH_NOTIFY_PROVIDER`: selected notifier, such as `dry-run`, `email`, `qq`, `wechat`, or `webhook`.
- `QRWATCH_DRY_RUN`: dry-run mode flag, such as `true` or `false`.
- `QRWATCH_CREDENTIAL_SOURCES`: comma-separated credential source labels, such as `env` or `local-file`.
- `QRWATCH_CONFIG_FILE`: optional dotenv-style local config file path.

Planned provider-specific variables should follow this pattern:

- `QRWATCH_SMTP_HOST`, `QRWATCH_SMTP_PORT`, `QRWATCH_SMTP_USERNAME`, `QRWATCH_SMTP_PASSWORD`, `QRWATCH_NOTIFY_TO`: email notifier settings.
- `QRWATCH_WEBHOOK_URL`: webhook-style provider endpoint, if added.

Secrets must not be printed in logs, preserved in artifacts, or included in screenshots.

## Reproducible Setup Command

Current safe validation command:

```bash
python tools/validate_harness_structure.py
```

Environment import smoke test:

```bash
conda run -n qrwatch python -c "import cv2, mss, PIL, numpy, dotenv, requests, pytest, pystray; print('python ok'); print(cv2.__version__)"
```

Application dry-run entrypoint:

```bash
conda run -n qrwatch python -m qrwatch
```

Application test command:

```bash
conda run -n qrwatch python -m pytest
```
