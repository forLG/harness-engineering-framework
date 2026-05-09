"""Screenshot capture abstraction placeholder.

Real Windows desktop capture will be implemented in a later milestone behind this
module boundary.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Frame:
    """Captured frame metadata placeholder."""

    width: int
    height: int
    source: str


class CaptureBackendUnavailable(RuntimeError):
    """Raised when screenshot capture is requested before a backend exists."""


def capture_screen() -> Frame:
    """Placeholder until the mss-backed capture milestone."""

    raise CaptureBackendUnavailable("screenshot capture is not implemented yet")
