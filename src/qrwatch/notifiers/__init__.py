"""Notifier interfaces and skeleton providers."""

from qrwatch.config import AppConfig
from qrwatch.notifiers.base import DryRunNotifier, Notifier

__all__ = ["DryRunNotifier", "Notifier", "create_notifier"]


def create_notifier(config: AppConfig) -> Notifier:
    """Create the configured notifier.

    Milestone 2 intentionally returns a dry-run notifier for every provider so
    no external messages can be sent yet.
    """

    return DryRunNotifier(provider_name=config.notifier_provider)
