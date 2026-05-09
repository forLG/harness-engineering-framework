"""Logging and redaction helpers."""

from __future__ import annotations

SENSITIVE_VALUE = "[redacted]"


def redact(value: str | None) -> str:
    """Return a redacted marker for non-empty sensitive values."""

    if not value:
        return ""
    return SENSITIVE_VALUE
