# Plans

Status: applied.

This file is the product roadmap for the Windows Python QR Watch app and the harness work needed to support it. Keep active execution detail in `docs/exec-plans/active/` and completed plans in `docs/exec-plans/completed/`.

## Current Product Roadmap

### Milestone 1: Harness Activation And Environment

Status: implemented.

Goal: make the repository legible as a Windows Python QR monitoring app and provide a reproducible local environment.

Acceptance criteria:

- `AGENTS.md`, `ARCHITECTURE.md`, and `docs/ENVIRONMENT.md` describe the QR Watch product rather than the generic scaffold.
- `environment.yml` defines the `qrwatch` Conda environment.
- The starter environment installs screenshot, QR detection, image, config, HTTP, and test packages.
- `python tools/validate_harness_structure.py` passes.
- The environment import smoke test passes.

### Milestone 2: Package Skeleton And CLI

Status: implemented.

Goal: create the first runnable Python package without implementing real screenshot or notification behavior yet.

Acceptance criteria:

- `src/qrwatch/` exists with the product layers documented in `ARCHITECTURE.md`.
- A `qrwatch` CLI or module entrypoint starts in dry-run mode.
- Configuration loading supports interval, notifier provider, dry-run mode, and credential sources.
- `conda run -n qrwatch python -m pytest` runs at least one passing smoke test.

### Milestone 3: Screenshot Capture And QR Detection

Status: planned.

Goal: prove local screenshot capture and QR detection in the logged-in Windows desktop session.

Acceptance criteria:

- Screenshot capture uses `mss` behind `src/qrwatch/capture.py`.
- QR detection uses OpenCV behind `src/qrwatch/detectors/`.
- Static fixture tests cover at least one QR-positive and one QR-negative image.
- A manual smoke command can inspect the current screen without saving screenshots by default.

### Milestone 4: Deduplication And Events

Status: planned.

Goal: convert raw QR detections into notification-ready events without repeated spam.

Acceptance criteria:

- Detection results are normalized into structured events.
- Repeated QR payloads are suppressed for a configurable window.
- Local state uses a small JSON or SQLite store.
- Tests cover repeated detections, expiry, and multiple QR codes in one frame.

### Milestone 5: Notification Provider Interface

Status: planned.

Goal: add safe notification dispatch with dry-run behavior first.

Acceptance criteria:

- `src/qrwatch/notifiers/` defines a provider interface.
- Dry-run notifier logs redacted event metadata without sending messages.
- First real provider is selected and implemented, preferably email or webhook before QQ/WeChat.
- Real provider tests avoid external sends unless credentials and a test recipient are explicitly supplied by a human.

### Milestone 6: Background Run Model

Status: designed.

Goal: make the app practical to run continuously on Windows through a logged-in user-session tray process.

Acceptance criteria:

- The app can run as a long-lived background process with clean shutdown.
- Logs include startup, capture failures, detection counts, notification results, and redacted errors.
- A Windows tray process is implemented with Start, Pause, Resume, Capture once, Open logs, Open screenshots, and Exit controls.
- Documentation explains how to start, stop, and inspect the process.

### Milestone 7: Privacy, Reliability, And Packaging

Status: planned.

Goal: harden the app before real personal use.

Acceptance criteria:

- Screenshots are retained locally with count and age limits.
- QR payload storage policy is explicit: store raw, hash, redact, or discard.
- Notification credentials are never committed or written to artifacts.
- Packaging output and generated files are documented.
- Tests and manual validation cover normal operation, detector failures, notification failures, and restart behavior.
