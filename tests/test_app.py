from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from qrwatch.app import QRWatchApp
from qrwatch.capture import Frame
from qrwatch.config import load_config
from qrwatch.detectors import QRDetection
from qrwatch.state import DeduplicationDecision, DeduplicationResult


def test_capture_once_runs_qr_detection_without_sending_notifications(monkeypatch):
    captured_at = datetime(2026, 5, 10, tzinfo=timezone.utc)
    frame = Frame(
        width=4,
        height=3,
        source="monitor:1",
        pixels=np.zeros((3, 4, 3), dtype=np.uint8),
        captured_at=captured_at,
    )

    def fake_capture_screen(*, monitor_index):
        assert monitor_index == 1
        return frame

    def fake_detect_qr_codes(pixels, *, source):
        assert pixels is frame.pixels
        assert source == "monitor:1"
        return (
            QRDetection(
                payload="sensitive-payload",
                source=source,
                corners=((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)),
            ),
        )

    monkeypatch.setattr("qrwatch.app.capture_screen", fake_capture_screen)
    monkeypatch.setattr("qrwatch.app.detect_qr_codes", fake_detect_qr_codes)

    class FakeStateStore:
        def filter_events(self, events):
            assert len(events) == 1
            assert events[0].payload == "sensitive-payload"
            return DeduplicationResult(
                decisions=(
                    DeduplicationDecision(
                        event=events[0],
                        payload_seen_before=False,
                        should_notify=True,
                        reason="new payload",
                    ),
                )
            )

    app = QRWatchApp(load_config(env={}), state_store=FakeStateStore())
    summary = app.capture_once()

    assert summary.capture_enabled is True
    assert summary.capture_width == 4
    assert summary.capture_height == 3
    assert summary.captured_at == captured_at
    assert summary.qr_detection_enabled is True
    assert summary.qr_detections_count == 1
    assert summary.qr_events_count == 1
    assert summary.notification_events_count == 1
    assert summary.suppressed_events_count == 0
    assert summary.notifications_sent == 0
