# Evaluation

Status: applied.

This is the single entry point for QR Watch testing, reproduction commands, and
validation expectations. Other docs may say what behavior should exist; this
file says how humans and agents should check it.

## Required Checks

Run the structural validator after framework layout, core documentation, or
guardrail changes:

```bash
python tools/validate_harness_structure.py
```

Run the product test suite after source, packaging, config, notifier, detector,
state, or storage changes:

```bash
conda run -n qrwatch python -m pytest
```

Run the environment import smoke test after dependency or environment changes:

```bash
conda run -n qrwatch python -c "import cv2, mss, PIL, numpy, dotenv, requests, pytest, pystray; print('python ok'); print(cv2.__version__)"
```

Generated test output should go under `artifacts/test-*`. Do not place logs,
fake local app data, screenshots, state files, or temporary command output in
the repository root.

## Change-Based Checks

- `AGENTS.md`, `ARCHITECTURE.md`, `PLANS.md`, or `docs/*.md`: run `python tools/validate_harness_structure.py`.
- `environment.yml`: run the environment import smoke test.
- `tools/*.py`: run `python tools/validate_harness_structure.py` and the relevant tool command.
- `src/qrwatch/capture.py`: run unit tests and a manual one-shot capture when a logged-in desktop session is available.
- `src/qrwatch/detectors/`: run QR fixture tests.
- `src/qrwatch/notifiers/`: run dry-run or fake-provider tests; real sends require human approval.
- `src/qrwatch/state.py` or `src/qrwatch/storage.py`: run deduplication, state recovery, and retention tests.
- `src/qrwatch/tray.py`: run unit tests plus a manual tray smoke check on Windows when possible.
- `packaging/`, `src/qrwatch/packaged.py`, or `tools/build_windows_executable.ps1`: run packaging validation from `docs/PACKAGING.md` when the local machine can build the executable.

## Product Reproduction

Default dry-run startup:

```bash
conda run -n qrwatch python -m qrwatch
```

One-shot capture and detection:

```bash
conda run -n qrwatch python -m qrwatch --once --dry-run
```

Background loop:

```bash
conda run -n qrwatch python -m qrwatch --run --dry-run
```

Tray process:

```bash
conda run -n qrwatch python -m qrwatch --tray
```

## Manual Windows Checks

Some behavior requires a logged-in Windows desktop session:

- Tray icon appears and menu actions work.
- `--once --dry-run` can capture the current desktop.
- Screenshot files appear under `%LOCALAPPDATA%\QRWatch\screenshots\` only when screenshot saving is enabled or an explicit save path is provided.
- Pause and resume stop and restart capture work.
- Exit flushes logs and deduplication state.
- Packaged `QRWatch.exe` starts in dry-run mode without credentials.

Record redacted notes only when they explain a decision or regression.

## Acceptance Evidence

For substantial changes, report:

- commands run and whether they passed.
- relevant failing output if a command failed.
- manual checks performed or skipped, with the reason.
- whether any external send was performed.
- whether any screenshot, QR payload, credential, or log evidence was preserved.

Notification-provider changes should also report dry-run event evidence and
state whether human approval was given before any real QQ Mail, mailbox,
WeChat, webhook, or other provider credential was used.

Do not preserve screenshots, raw QR payloads, credentials, or external-provider
responses unless the user explicitly approves the evidence and it has been
reviewed or redacted.

Repository-local evidence belongs under `artifacts/`. The contents are ignored
by default; force-add only reviewed evidence that should become part of project
history.
