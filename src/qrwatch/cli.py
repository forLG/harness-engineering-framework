"""Command-line interface for QR Watch."""

from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path
from typing import Sequence

from qrwatch.app import QRWatchApp
from qrwatch.capture import CaptureBackendUnavailable, CaptureError
from qrwatch.config import (
    ConfigError,
    load_config,
    parse_credential_sources,
    parse_dedup_window,
)
from qrwatch.detectors import DetectorBackendUnavailable, QRDetectionError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qrwatch",
        description="Run the QR Watch local watcher.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to a local dotenv-style QR Watch config file.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        help="Screenshot interval in seconds.",
    )
    parser.add_argument(
        "--provider",
        help="Notifier provider name, such as dry-run, email, webhook, qq, or wechat.",
    )
    parser.add_argument(
        "--credential-sources",
        help="Comma-separated credential source names, such as env or local-file.",
    )
    parser.add_argument(
        "--capture-once",
        action="store_true",
        help="Capture one screen frame and print metadata without saving it.",
    )
    parser.add_argument(
        "--save-capture",
        type=Path,
        metavar="PATH",
        help="Save one captured frame as a PNG at PATH; implies --capture-once.",
    )
    parser.add_argument(
        "--monitor",
        type=int,
        default=1,
        help="mss monitor index to capture; use 1 for primary or 0 for all monitors.",
    )
    parser.add_argument(
        "--dedup-window",
        help="Seconds to suppress repeated QR payload notifications.",
    )
    parser.add_argument(
        "--state-path",
        type=Path,
        help="Path to the local JSON deduplication state file.",
    )
    dry_run = parser.add_mutually_exclusive_group()
    dry_run.add_argument(
        "--dry-run",
        action="store_true",
        default=None,
        help="Force dry-run mode.",
    )
    dry_run.add_argument(
        "--no-dry-run",
        action="store_false",
        dest="dry_run",
        help="Disable dry-run mode after a real provider is implemented.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = load_config(config_path=args.config)
        if args.interval is not None:
            config = replace(config, interval_seconds=args.interval).validated()
        if args.provider is not None:
            config = replace(config, notifier_provider=args.provider).validated()
        if args.credential_sources is not None:
            config = replace(
                config,
                credential_sources=parse_credential_sources(args.credential_sources),
            ).validated()
        if args.dedup_window is not None:
            config = replace(
                config,
                dedup_window_seconds=parse_dedup_window(args.dedup_window),
            ).validated()
        if args.state_path is not None:
            config = replace(config, state_path=args.state_path).validated()
        if args.dry_run is not None:
            config = replace(config, dry_run=args.dry_run).validated()

        app = QRWatchApp(config)
        if args.capture_once or args.save_capture is not None:
            summary = app.capture_once(
                monitor_index=args.monitor,
                save_path=args.save_capture,
            )
        else:
            summary = app.run_once()
    except ConfigError as exc:
        parser.error(str(exc))
        return 2
    except (
        CaptureBackendUnavailable,
        CaptureError,
        DetectorBackendUnavailable,
        QRDetectionError,
    ) as exc:
        parser.error(str(exc))
        return 2

    mode = "dry-run" if summary.dry_run else "live"
    print(f"QR Watch started in {mode} mode")
    print(f"provider={summary.notifier_provider}")
    print(f"interval_seconds={summary.interval_seconds:g}")
    print(f"credential_sources={','.join(summary.credential_sources)}")
    if summary.capture_enabled:
        print("capture=enabled")
        print(f"capture_source={summary.capture_source}")
        print(f"capture_size={summary.capture_width}x{summary.capture_height}")
        if summary.captured_at is not None:
            print(f"captured_at={summary.captured_at.isoformat()}")
        if summary.capture_saved_path is not None:
            print(f"capture_saved={summary.capture_saved_path}")
        print(
            "qr_detection=enabled"
            if summary.qr_detection_enabled
            else "qr_detection=disabled"
        )
        print(f"qr_detections={summary.qr_detections_count}")
        print(f"qr_events={summary.qr_events_count}")
        print(f"notification_events={summary.notification_events_count}")
        print(f"suppressed_events={summary.suppressed_events_count}")
    else:
        print("capture=disabled")
    print(f"notifications_sent={summary.notifications_sent}")
    return 0
