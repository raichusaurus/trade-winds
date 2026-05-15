from __future__ import annotations

import pytest


def test_settings_loads_required_values_from_environment(monkeypatch, tmp_path) -> None:
    from trade_winds.config import Settings

    monkeypatch.setenv("TRADE_WINDS_SLEEPER_USERNAME", "john_seed")
    monkeypatch.setenv("TRADE_WINDS_SEASON", "2026")
    monkeypatch.setenv("TRADE_WINDS_DB_PATH", str(tmp_path / "trade-winds.sqlite3"))
    monkeypatch.setenv("TRADE_WINDS_OUTPUT_DIR", str(tmp_path / "exports"))
    monkeypatch.setenv("TRADE_WINDS_REQUEST_RATE_PER_SECOND", "1.25")
    monkeypatch.setenv("TRADE_WINDS_MAX_USERS", "25")
    monkeypatch.setenv("TRADE_WINDS_MAX_LEAGUES", "12")
    monkeypatch.setenv("TRADE_WINDS_MAX_API_CALLS", "250")

    settings = Settings.load()

    assert settings.sleeper_username == "john_seed"
    assert settings.season == 2026
    assert settings.database_path == tmp_path / "trade-winds.sqlite3"
    assert settings.output_dir == tmp_path / "exports"
    assert settings.request_rate_per_second == 1.25
    assert settings.max_users == 25
    assert settings.max_leagues == 12
    assert settings.max_api_calls == 250


def test_settings_requires_seed_username(monkeypatch) -> None:
    from trade_winds.config import ConfigError, Settings

    monkeypatch.delenv("TRADE_WINDS_SLEEPER_USERNAME", raising=False)

    with pytest.raises(ConfigError, match="TRADE_WINDS_SLEEPER_USERNAME"):
        Settings.load()


@pytest.mark.parametrize(
    ("env_name", "env_value"),
    [
        ("TRADE_WINDS_SEASON", "not-a-season"),
        ("TRADE_WINDS_REQUEST_RATE_PER_SECOND", "0"),
        ("TRADE_WINDS_MAX_USERS", "-1"),
        ("TRADE_WINDS_MAX_LEAGUES", "-1"),
        ("TRADE_WINDS_MAX_API_CALLS", "0"),
    ],
)
def test_settings_rejects_invalid_numeric_values(monkeypatch, env_name, env_value) -> None:
    from trade_winds.config import ConfigError, Settings

    monkeypatch.setenv("TRADE_WINDS_SLEEPER_USERNAME", "john_seed")
    monkeypatch.setenv(env_name, env_value)

    with pytest.raises(ConfigError, match=env_name):
        Settings.load()
