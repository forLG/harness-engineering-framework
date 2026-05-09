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
        }
    )

    assert config.interval_seconds == 12.5
    assert config.notifier_provider == "webhook"
    assert config.dry_run is False
    assert config.credential_sources == ("env", "local-file")
    assert config.dedup_window_seconds == 45.0
    assert config.state_path == state_path


def test_default_state_path_uses_local_app_data():
    local_app_data = Path("artifacts/test-localappdata")
    config = load_config(env={"LOCALAPPDATA": str(local_app_data)})

    assert config.state_path == local_app_data / "QRWatch" / "dedup-state.json"


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
