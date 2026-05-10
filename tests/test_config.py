import pytest
from pathlib import Path

from qrwatch.config import ConfigError, load_config


def test_load_config_defaults_to_safe_dry_run():
    config = load_config(env={})

    assert config.interval_seconds == 30.0
    assert config.notifier_provider == "dry-run"
    assert config.dry_run is True
    assert config.credential_sources == ("env",)
    assert config.dedup_window_seconds == 300.0
    assert config.smtp_host == "smtp.qq.com"
    assert config.smtp_port == 465
    assert config.smtp_use_ssl is True
    assert config.log_level == "INFO"
    assert config.monitor_index == 1
    assert config.save_screenshots is False
    assert config.screenshot_max_count == 200
    assert config.screenshot_max_age_days == 1.0


def test_load_config_from_env():
    state_path = Path("artifacts/test-state/config-state.json")

    config = load_config(
        env={
            "QRWATCH_INTERVAL_SECONDS": "12.5",
            "QRWATCH_NOTIFY_PROVIDER": "webhook",
            "QRWATCH_DRY_RUN": "false",
            "QRWATCH_CREDENTIAL_SOURCES": "env,local-file",
            "QRWATCH_DEDUP_WINDOW_SECONDS": "45",
            "QRWATCH_STATE_PATH": str(state_path),
            "QRWATCH_LOG_DIR": "artifacts/test-logs",
            "QRWATCH_SCREENSHOT_DIR": "artifacts/test-screenshots",
            "QRWATCH_SAVE_SCREENSHOTS": "true",
            "QRWATCH_SCREENSHOT_MAX_COUNT": "12",
            "QRWATCH_SCREENSHOT_MAX_AGE_DAYS": "2.5",
            "QRWATCH_LOG_LEVEL": "debug",
            "QRWATCH_MONITOR_INDEX": "0",
            "QRWATCH_SMTP_HOST": "smtp.example.test",
            "QRWATCH_SMTP_PORT": "587",
            "QRWATCH_SMTP_USERNAME": "sender@example.test",
            "QRWATCH_SMTP_PASSWORD": "secret",
            "QRWATCH_SMTP_USE_SSL": "false",
            "QRWATCH_SMTP_TIMEOUT_SECONDS": "3",
            "QRWATCH_NOTIFY_FROM": "qrwatch@example.test",
            "QRWATCH_NOTIFY_TO": "receiver@example.test",
        }
    )

    assert config.interval_seconds == 12.5
    assert config.notifier_provider == "webhook"
    assert config.dry_run is False
    assert config.credential_sources == ("env", "local-file")
    assert config.dedup_window_seconds == 45.0
    assert config.state_path == state_path
    assert config.log_dir == Path("artifacts/test-logs")
    assert config.screenshot_dir == Path("artifacts/test-screenshots")
    assert config.save_screenshots is True
    assert config.screenshot_max_count == 12
    assert config.screenshot_max_age_days == 2.5
    assert config.log_level == "DEBUG"
    assert config.monitor_index == 0
    assert config.smtp_host == "smtp.example.test"
    assert config.smtp_port == 587
    assert config.smtp_username == "sender@example.test"
    assert config.smtp_password == "secret"
    assert config.smtp_use_ssl is False
    assert config.smtp_timeout_seconds == 3.0
    assert config.notify_from == "qrwatch@example.test"
    assert config.notify_to == "receiver@example.test"


def test_default_state_path_uses_local_app_data():
    local_app_data = Path("artifacts/test-localappdata")
    config = load_config(env={"LOCALAPPDATA": str(local_app_data)})

    assert config.state_path == local_app_data / "QRWatch" / "dedup-state.json"
    assert config.log_dir == local_app_data / "QRWatch" / "logs"
    assert config.screenshot_dir == local_app_data / "QRWatch" / "screenshots"


def test_env_overrides_config_file():
    config = load_config(
        env={"QRWATCH_INTERVAL_SECONDS": "10"},
        config_path="tests/fixtures/qrwatch.env",
    )

    assert config.interval_seconds == 10.0
    assert config.notifier_provider == "email"
    assert config.credential_sources == ("local-file",)


def test_rejects_invalid_interval():
    with pytest.raises(ConfigError, match="interval"):
        load_config(env={"QRWATCH_INTERVAL_SECONDS": "0"})


def test_rejects_invalid_dedup_window():
    with pytest.raises(ConfigError, match="deduplication window"):
        load_config(env={"QRWATCH_DEDUP_WINDOW_SECONDS": "0"})


def test_rejects_invalid_monitor_index():
    with pytest.raises(ConfigError, match="monitor index"):
        load_config(env={"QRWATCH_MONITOR_INDEX": "-1"})


def test_rejects_invalid_screenshot_retention():
    with pytest.raises(ConfigError, match="screenshot max count"):
        load_config(env={"QRWATCH_SCREENSHOT_MAX_COUNT": "0"})

    with pytest.raises(ConfigError, match="screenshot max age"):
        load_config(env={"QRWATCH_SCREENSHOT_MAX_AGE_DAYS": "0"})


def test_rejects_live_dry_run_provider():
    with pytest.raises(ConfigError, match="real notifier provider"):
        load_config(env={"QRWATCH_DRY_RUN": "false"})


def test_rejects_live_email_without_credentials():
    with pytest.raises(ConfigError, match="SMTP username"):
        load_config(
            env={
                "QRWATCH_NOTIFY_PROVIDER": "email",
                "QRWATCH_DRY_RUN": "false",
            }
        )


def test_loads_live_qq_mail_config():
    config = load_config(
        env={
            "QRWATCH_NOTIFY_PROVIDER": "qq-mail",
            "QRWATCH_DRY_RUN": "false",
            "QRWATCH_SMTP_USERNAME": "sender@qq.com",
            "QRWATCH_SMTP_PASSWORD": "authorization-code",
            "QRWATCH_NOTIFY_TO": "receiver@example.com",
        }
    )

    assert config.notifier_provider == "qq-mail"
    assert config.dry_run is False
    assert config.smtp_host == "smtp.qq.com"
    assert config.smtp_port == 465
    assert config.smtp_username == "sender@qq.com"
    assert config.notify_to == "receiver@example.com"
