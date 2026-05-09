"""Command-line interface for QR Watch."""

from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path
from typing import Sequence

from qrwatch.app import QRWatchApp
from qrwatch.config import ConfigError, load_config, parse_credential_sources


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
        if args.dry_run is not None:
            config = replace(config, dry_run=args.dry_run).validated()

        summary = QRWatchApp(config).run_once()
    except ConfigError as exc:
        parser.error(str(exc))
        return 2

    mode = "dry-run" if summary.dry_run else "live"
    print(f"QR Watch started in {mode} mode")
    print(f"provider={summary.notifier_provider}")
    print(f"interval_seconds={summary.interval_seconds:g}")
    print(f"credential_sources={','.join(summary.credential_sources)}")
    print("capture=disabled")
    print(f"notifications_sent={summary.notifications_sent}")
    return 0
