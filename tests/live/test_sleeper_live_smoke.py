from __future__ import annotations

import os

import pytest

pytestmark = pytest.mark.live


@pytest.mark.skipif(
    os.getenv("TRADE_WINDS_LIVE_SLEEPER") != "1",
    reason="Live Sleeper smoke tests are opt-in only.",
)
def test_live_sleeper_seed_user_and_leagues_smoke(monkeypatch) -> None:
    from trade_winds.config import Settings
    from trade_winds.sleeper.client import SleeperClient

    settings = Settings.load()
    client = SleeperClient.from_settings(settings)

    user_response = client.get_user_by_username(settings.sleeper_username)
    leagues_response = client.get_user_leagues(user_response.user.user_id, settings.season)

    assert user_response.user.user_id
    assert leagues_response.raw is not None
    assert client.request_count >= 2
