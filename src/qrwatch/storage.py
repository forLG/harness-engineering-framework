"""Local screenshot storage and retention helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCREENSHOT_GLOB = "*.png"


@dataclass(frozen=True)
class ScreenshotRetentionSummary:
    deleted_count: int
    retained_count: int


def retained_screenshot_path(
    screenshot_dir: str | Path,
    *,
    captured_at: datetime,
    source: str,
) -> Path:
    """Return a deterministic local screenshot path for a captured frame."""

    timestamp = _ensure_utc(captured_at).strftime("%Y%m%dT%H%M%S%fZ")
    safe_source = "".join(
        character if character.isalnum() else "-"
        for character in source.lower()
    ).strip("-")
    suffix = f"-{safe_source}" if safe_source else ""
    return Path(screenshot_dir) / f"qrwatch-{timestamp}{suffix}.png"


def prune_screenshots(
    screenshot_dir: str | Path,
    *,
    max_count: int,
    max_age_days: float,
    now: datetime | None = None,
) -> ScreenshotRetentionSummary:
    """Delete retained screenshots over the configured count or age limits."""

    if max_count <= 0:
        raise ValueError("screenshot max count must be greater than zero")
    if max_age_days <= 0:
        raise ValueError("screenshot max age must be greater than zero days")

    directory = Path(screenshot_dir)
    if not directory.exists():
        return ScreenshotRetentionSummary(deleted_count=0, retained_count=0)

    deleted = 0
    cutoff = _ensure_utc(now or datetime.now(timezone.utc)) - timedelta(
        days=max_age_days,
    )
    cutoff_timestamp = cutoff.timestamp()
    retained: list[Path] = []

    for path in directory.glob(SCREENSHOT_GLOB):
        if not path.is_file():
            continue
        stat = path.stat()
        if stat.st_mtime < cutoff_timestamp:
            path.unlink()
            deleted += 1
        else:
            retained.append(path)

    retained.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    for path in retained[max_count:]:
        path.unlink()
        deleted += 1

    return ScreenshotRetentionSummary(
        deleted_count=deleted,
        retained_count=min(len(retained), max_count),
    )


def _ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)
