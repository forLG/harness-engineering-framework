# Runtime

Status: applied.

This document defines both the QR Watch product runtime and the Codex harness runtime. QR Watch is a Windows Python background app controlled by a small system tray UI.

## Product Run Model

Recommended process model: a logged-in Windows user-session process with a system tray icon.

Why this model fits the app:

- Screenshot capture works naturally in the interactive desktop session.
- The app can run quietly in the background without a full window.
- The user still has simple controls for Start, Pause, Resume, Stop, status, and opening logs/screenshots.
- It avoids the complexity of Windows service desktop isolation during the first implementation.

The tray controller should use `pystray`; any small settings/status window can use built-in `tkinter` later if needed.

## Product Entrypoints

Planned commands:

```bash
conda run -n qrwatch python -m qrwatch --tray
conda run -n qrwatch python -m qrwatch --run
conda run -n qrwatch python -m qrwatch --once
conda run -n qrwatch python -m qrwatch --dry-run
```

Expected behavior:

- `--tray`: start the tray UI and own the worker lifecycle.
- `--run`: run the background screenshot loop without tray UI, useful for debugging and scheduled runs.
- `--once`: capture one frame, run QR detection, write logs/screenshots according to config, then exit.
- `--dry-run`: never send external messages; log the notification event instead.

These commands are planned until `src/qrwatch/` is implemented.

## Tray UI Controls

Minimum tray menu:

- Status: running, paused, stopped, degraded, or error.
- Start monitoring.
- Pause monitoring.
- Resume monitoring.
- Capture once.
- Open logs folder.
- Open screenshots folder.
- Open settings file.
- Exit.

The tray process should keep the UI responsive while the worker loop runs in a background thread. UI actions should communicate with the worker through a small controller object rather than calling capture or notifier code directly.

## Worker Loop

The worker loop owns app behavior:

1. Load config.
2. Initialize logging, screenshot storage, QR detector, deduplication state, and notifier.
3. Wait until monitoring is running.
4. Capture the current screen.
5. Store screenshot evidence according to retention settings.
6. Detect QR codes.
7. Normalize detections into events.
8. Deduplicate repeated payloads.
9. Notify configured provider or dry-run logger.
10. Sleep until the next configured interval.
11. On pause, stop capture and notification work but keep the tray alive.
12. On shutdown, flush logs and state.

Default interval: 5 seconds for development. The user can increase it after reliability and storage behavior are proven.

## Runtime State

Real app runs should write local runtime state outside the Git repository:

- Base directory: `%LOCALAPPDATA%\QRWatch\`
- Logs: `%LOCALAPPDATA%\QRWatch\logs\`
- Screenshots: `%LOCALAPPDATA%\QRWatch\screenshots\`
- State: `%LOCALAPPDATA%\QRWatch\state\`
- Config: `%LOCALAPPDATA%\QRWatch\config.env` or repository-local `.env` during development.

Repository `artifacts/` directories remain harness evidence buckets. Do not use them as the default product runtime store.

## Configuration

Planned environment variables:

- `QRWATCH_INTERVAL_SECONDS`: screenshot interval.
- `QRWATCH_DRY_RUN`: when true, do not send external messages.
- `QRWATCH_NOTIFY_PROVIDER`: `dry-run`, `email`, `qq-mail`, `qqmail`, `webhook`, `qq`, or `wechat`. Only `dry-run`, `email`, `qq-mail`, and `qqmail` have implemented behavior now.
- `QRWATCH_SMTP_HOST`, `QRWATCH_SMTP_PORT`, `QRWATCH_SMTP_USERNAME`, `QRWATCH_SMTP_PASSWORD`, `QRWATCH_NOTIFY_TO`: SMTP email notifier settings for live QQ Mail-compatible sends.
- `QRWATCH_SCREENSHOT_MODE`: `recent`, `detections`, `errors`, or `all`.
- `QRWATCH_SCREENSHOT_RETENTION_COUNT`: maximum recent screenshots to keep.
- `QRWATCH_DEDUP_SECONDS`: suppress repeated QR payloads during this window.
- `QRWATCH_LOG_LEVEL`: `DEBUG`, `INFO`, `WARNING`, or `ERROR`.

Provider-specific credentials stay in local env/config only and must never be committed.

## Harness Invocation Modes

- Human-supervised interactive runs: `codex -C <project>`.
- Harness task loop preview: `python tools/harness_loop.py --once`.
- Harness task loop execution: `python tools/harness_loop.py --once --execute`.
- Harness smoke evals: `python tools/run_evals.py --suite smoke`.
- Entropy report: `python tools/entropy_control.py --report`.

When `--execute` is used, the supervisor invokes role agents with `codex exec --full-auto -C <repo> ...`. The supervisor writes role prompts, role outputs, and summaries under `artifacts/runs/<run-id>/`.

## Harness State And Artifacts

- Task queue: `runtime/tasks/queue/`
- Active tasks: `runtime/tasks/active/`
- Completed tasks: `runtime/tasks/completed/`
- Blocked tasks: `runtime/tasks/blocked/`
- Run artifacts: `artifacts/runs/`
- Review artifacts: `artifacts/reviews/`
- Validation artifacts: `artifacts/validation/`
- Harness logs: `artifacts/logs/`
- Harness traces: `artifacts/traces/`
- Harness screenshots: `artifacts/screenshots/`
- Eval results: `evals/results/`

## Validation Commands

Harness structure:

```bash
python tools/validate_harness_structure.py
```

Environment smoke test:

```bash
conda run -n qrwatch python -c "import cv2, mss, PIL, numpy, dotenv, requests, pytest, pystray; print('python ok'); print(cv2.__version__)"
```

Product tests after source exists:

```bash
conda run -n qrwatch python -m pytest
```

## Stop Conditions

Product runtime:

- Stop: user selects Exit, sends a termination signal, or unrecoverable initialization fails.
- Pause: user selects Pause; the tray remains active and the worker loop stops capturing.
- Degraded: screenshot capture, QR detection, or notification fails but the app can keep running after logging the failure.
- Error: repeated failures exceed the configured threshold or credentials/config are invalid.

Harness runtime:

- Success: validator returns `passed` and reviewer returns `approved`.
- Follow-up: validator returns `failed` or reviewer returns `needs_followup`.
- Blocked: required human input, credentials, external sends, or policy decisions are needed.
