from __future__ import annotations

import pytest


@pytest.mark.integration
def test_discovery_resume_does_not_duplicate_persisted_users_or_leagues(
    tmp_path, fixture_json
) -> None:
    from trade_winds.app import AppContext
    from trade_winds.config import Settings
    from trade_winds.sleeper.testing import FakeSleeperClient

    settings = Settings(
        sleeper_username="john_seed",
        season=2026,
        database_path=tmp_path / "trade-winds.sqlite3",
        request_rate_per_second=1.0,
        max_users=10,
        max_leagues=5,
        max_api_calls=20,
        output_dir=tmp_path / "exports",
    )
    fake_client = FakeSleeperClient(
        seed_user=fixture_json("sleeper/user_seed.json"),
        leagues=fixture_json("sleeper/user_leagues_current_season.json"),
        league_users=fixture_json("sleeper/league_users.json"),
        rosters=fixture_json("sleeper/league_rosters.json"),
        fail_after_calls=2,
    )

    interrupted_context = AppContext.create(settings=settings, sleeper_client=fake_client)

    with pytest.raises(RuntimeError, match="simulated interruption"):
        interrupted_context.crawl_service.discover()

    resumed_context = AppContext.create(
        settings=settings,
        sleeper_client=FakeSleeperClient(
            seed_user=fixture_json("sleeper/user_seed.json"),
            leagues=fixture_json("sleeper/user_leagues_current_season.json"),
            league_users=fixture_json("sleeper/league_users.json"),
            rosters=fixture_json("sleeper/league_rosters.json"),
        ),
    )
    summary = resumed_context.crawl_service.discover()

    assert summary.status == "completed"
    assert summary.users_upserted == 3
    assert summary.leagues_upserted == 1
    assert summary.duplicate_users_skipped >= 1
    assert resumed_context.repositories.users.count() == 3
    assert resumed_context.repositories.leagues.count() == 1
