"""Application composition and dry-run lifecycle."""

from __future__ import annotations

from dataclasses import dataclass

from qrwatch.config import AppConfig
from qrwatch.notifiers import create_notifier


@dataclass(frozen=True)
class RunSummary:
    """Summary of a skeleton run that performs no capture or external sends."""

    dry_run: bool
    interval_seconds: float
    notifier_provider: str
    credential_sources: tuple[str, ...]
    capture_enabled: bool = False
    notifications_sent: int = 0


class QRWatchApp:
    """Compose product layers without enabling screenshot or notifier behavior yet."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.notifier = create_notifier(config)

    def run_once(self) -> RunSummary:
        """Run the milestone-2 dry-run path."""

        self.notifier.notify_dry_run()
        return RunSummary(
            dry_run=self.config.dry_run,
            interval_seconds=self.config.interval_seconds,
            notifier_provider=self.config.notifier_provider,
            credential_sources=self.config.credential_sources,
        )
