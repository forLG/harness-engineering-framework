"""Configuration loading for QR Watch."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

from dotenv import dotenv_values


DEFAULT_INTERVAL_SECONDS = 30.0
DEFAULT_NOTIFIER_PROVIDER = "dry-run"
DEFAULT_CREDENTIAL_SOURCES = ("env",)
DEFAULT_DEDUP_WINDOW_SECONDS = 300.0

ENV_CONFIG_FILE = "QRWATCH_CONFIG_FILE"
ENV_INTERVAL_SECONDS = "QRWATCH_INTERVAL_SECONDS"
ENV_NOTIFIER_PROVIDER = "QRWATCH_NOTIFY_PROVIDER"
ENV_DRY_RUN = "QRWATCH_DRY_RUN"
ENV_CREDENTIAL_SOURCES = "QRWATCH_CREDENTIAL_SOURCES"
ENV_DEDUP_WINDOW_SECONDS = "QRWATCH_DEDUP_WINDOW_SECONDS"
ENV_STATE_PATH = "QRWATCH_STATE_PATH"


class ConfigError(ValueError):
    """Raised when QR Watch configuration is invalid."""


@dataclass(frozen=True)
class AppConfig:
    interval_seconds: float = DEFAULT_INTERVAL_SECONDS
    notifier_provider: str = DEFAULT_NOTIFIER_PROVIDER
    dry_run: bool = True
    credential_sources: tuple[str, ...] = DEFAULT_CREDENTIAL_SOURCES
    config_path: Path | None = None
    dedup_window_seconds: float = DEFAULT_DEDUP_WINDOW_SECONDS
    state_path: Path = field(default_factory=lambda: default_state_path(os.environ))

    def validated(self) -> "AppConfig":
        if self.interval_seconds <= 0:
            raise ConfigError("interval must be greater than zero seconds")
        if not self.notifier_provider.strip():
            raise ConfigError("notifier provider must not be empty")
        if not self.credential_sources:
            raise ConfigError("at least one credential source is required")
        if any(not source.strip() for source in self.credential_sources):
            raise ConfigError("credential sources must not contain empty values")
        if self.dedup_window_seconds <= 0:
            raise ConfigError("deduplication window must be greater than zero seconds")
        return self


def load_config(
    *,
    env: Mapping[str, str] | None = None,
    config_path: str | Path | None = None,
) -> AppConfig:
    """Load configuration from an optional dotenv file and environment variables.

    Values from environment variables override values from the config file.
    Secrets may be referenced by credential source, but are not read or returned
    by this milestone-2 configuration object.
    """

    current_env = os.environ if env is None else env
    selected_path = _resolve_config_path(config_path, current_env)
    values: dict[str, str] = {}

    if selected_path is not None:
        if not selected_path.exists():
            raise ConfigError(f"config file does not exist: {selected_path}")
        values.update(
            {
                key: value
                for key, value in dotenv_values(selected_path).items()
                if value is not None
            }
        )

    values.update(
        {
            key: current_env[key]
            for key in (
                ENV_INTERVAL_SECONDS,
                ENV_NOTIFIER_PROVIDER,
                ENV_DRY_RUN,
                ENV_CREDENTIAL_SOURCES,
                ENV_DEDUP_WINDOW_SECONDS,
                ENV_STATE_PATH,
            )
            if key in current_env
        }
    )

    return AppConfig(
        interval_seconds=parse_interval(
            values.get(ENV_INTERVAL_SECONDS, str(DEFAULT_INTERVAL_SECONDS))
        ),
        notifier_provider=values.get(
            ENV_NOTIFIER_PROVIDER, DEFAULT_NOTIFIER_PROVIDER
        ).strip(),
        dry_run=parse_bool(values.get(ENV_DRY_RUN, "true")),
        credential_sources=parse_credential_sources(
            values.get(ENV_CREDENTIAL_SOURCES, ",".join(DEFAULT_CREDENTIAL_SOURCES))
        ),
        config_path=selected_path,
        dedup_window_seconds=parse_dedup_window(
            values.get(ENV_DEDUP_WINDOW_SECONDS, str(DEFAULT_DEDUP_WINDOW_SECONDS))
        ),
        state_path=Path(
            values.get(ENV_STATE_PATH)
            or str(default_state_path(current_env))
        ),
    ).validated()


def parse_interval(value: str) -> float:
    try:
        interval = float(value)
    except ValueError as exc:
        raise ConfigError("interval must be a number of seconds") from exc
    if interval <= 0:
        raise ConfigError("interval must be greater than zero seconds")
    return interval


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise ConfigError(f"invalid boolean value: {value}")


def parse_credential_sources(value: str) -> tuple[str, ...]:
    sources = tuple(part.strip() for part in value.split(",") if part.strip())
    if not sources:
        raise ConfigError("at least one credential source is required")
    return sources


def parse_dedup_window(value: str) -> float:
    try:
        window = float(value)
    except ValueError as exc:
        raise ConfigError("deduplication window must be a number of seconds") from exc
    if window <= 0:
        raise ConfigError("deduplication window must be greater than zero seconds")
    return window


def default_state_path(env: Mapping[str, str] | None = None) -> Path:
    current_env = os.environ if env is None else env
    if current_env.get("LOCALAPPDATA"):
        return Path(current_env["LOCALAPPDATA"]) / "QRWatch" / "dedup-state.json"
    return Path.home() / "AppData" / "Local" / "QRWatch" / "dedup-state.json"


def _resolve_config_path(
    config_path: str | Path | None,
    env: Mapping[str, str],
) -> Path | None:
    if config_path is not None:
        return Path(config_path)
    if env.get(ENV_CONFIG_FILE):
        return Path(env[ENV_CONFIG_FILE])
    return None
