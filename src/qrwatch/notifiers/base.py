"""Notifier provider interfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Notifier(Protocol):
    provider_name: str

    def notify_dry_run(self) -> None:
        """Exercise notifier composition without sending anything."""


@dataclass(frozen=True)
class DryRunNotifier:
    provider_name: str = "dry-run"

    def notify_dry_run(self) -> None:
        return None
