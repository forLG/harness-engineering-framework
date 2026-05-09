"""Application composition and dry-run lifecycle."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from qrwatch.capture import capture_screen, save_frame_png
from qrwatch.config import AppConfig
from qrwatch.detectors import detect_qr_codes
from qrwatch.notifiers import create_notifier


@dataclass(frozen=True)
class RunSummary:
    """Summary of a skeleton run that performs no capture or external sends."""

    dry_run: bool
    interval_seconds: float
    notifier_provider: str
    credential_sources: tuple[str, ...]
    capture_enabled: bool = False
    capture_width: int | None = None
    capture_height: int | None = None
    capture_source: str | None = None
    captured_at: datetime | None = None
    capture_saved_path: Path | None = None
    qr_detection_enabled: bool = False
    qr_detections_count: int = 0
    notifications_sent: int = 0


class QRWatchApp:
    """Compose product layers without enabling continuous watcher behavior yet."""

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

    def capture_once(
        self,
        *,
        monitor_index: int = 1,
        save_path: str | Path | None = None,
    ) -> RunSummary:
        """Capture one screen frame without saving it or sending notifications."""

        frame = capture_screen(monitor_index=monitor_index)
        detections = detect_qr_codes(frame.pixels, source=frame.source)
        saved_path = save_frame_png(frame, save_path) if save_path is not None else None
        return RunSummary(
            dry_run=self.config.dry_run,
            interval_seconds=self.config.interval_seconds,
            notifier_provider=self.config.notifier_provider,
            credential_sources=self.config.credential_sources,
            capture_enabled=True,
            capture_width=frame.width,
            capture_height=frame.height,
            capture_source=frame.source,
            captured_at=frame.captured_at,
            capture_saved_path=saved_path,
            qr_detection_enabled=True,
            qr_detections_count=len(detections),
        )
