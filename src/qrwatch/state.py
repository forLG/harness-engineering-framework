"""Deduplication state placeholder."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeduplicationDecision:
    payload_seen_before: bool
    should_notify: bool
