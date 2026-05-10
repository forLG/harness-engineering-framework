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


def test_capture_once_dispatches_deduplicated_notification_events(monkeypatch):
    captured_at = datetime(2026, 5, 10, tzinfo=timezone.utc)
    frame = Frame(
        width=4,
        height=3,
        source="monitor:1",
        pixels=np.zeros((3, 4, 3), dtype=np.uint8),
        captured_at=captured_at,
    )

    monkeypatch.setattr(
        "qrwatch.app.capture_screen",
        lambda *, monitor_index: frame,
    )
    monkeypatch.setattr(
        "qrwatch.app.detect_qr_codes",
        lambda pixels, *, source: (
            QRDetection(
                payload="qrwatch:test-payload",
                source=source,
                corners=(),
            ),
        ),
    )

    class FakeStateStore:
        def filter_events(self, events):
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

    class FakeNotifier:
        provider_name = "email"

        def __init__(self):
            self.events = []

        def notify(self, event):
            from qrwatch.notifiers.base import NotificationResult

            self.events.append(event)
            return NotificationResult(
                provider_name=self.provider_name,
                sent=True,
                dry_run=False,
                payload_hash=event.payload_hash,
                payload_length=len(event.payload),
            )

        def notify_dry_run(self):
            raise AssertionError("capture_once should dispatch event notifications")

    notifier = FakeNotifier()
    config = load_config(
        env={
            "QRWATCH_NOTIFY_PROVIDER": "email",
            "QRWATCH_DRY_RUN": "false",
            "QRWATCH_SMTP_USERNAME": "sender@qq.com",
            "QRWATCH_SMTP_PASSWORD": "authorization-code",
            "QRWATCH_NOTIFY_TO": "receiver@example.com",
        }
    )
    app = QRWatchApp(
        config,
        state_store=FakeStateStore(),
        notifier=notifier,
    )

    summary = app.capture_once()

    assert len(notifier.events) == 1
    assert notifier.events[0].payload == "qrwatch:test-payload"
    assert summary.notification_events_count == 1
    assert summary.notifications_sent == 1
    assert summary.notifications_failed == 0
