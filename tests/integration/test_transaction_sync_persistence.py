from __future__ import annotations

import pytest


@pytest.mark.integration
def test_transaction_sync_persists_raw_payloads_and_normalized_facts_idempotently(
    tmp_path,
    fixture_json,
) -> None:
    from trade_winds.app import AppContext
    from trade_winds.config import Settings
    from trade_winds.sleeper.testing import FakeSleeperClient

    db_path = tmp_path / "trade-winds.sqlite3"
    settings = Settings(
        sleeper_username="john_seed",
        season=2026,
        database_path=db_path,
        request_rate_per_second=1.0,
        max_users=10,
        max_leagues=5,
        max_api_calls=50,
        output_dir=tmp_path / "exports",
    )
    fake_client = FakeSleeperClient(
        seed_user=fixture_json("sleeper/user_seed.json"),
        leagues=fixture_json("sleeper/user_leagues_current_season.json"),
        league_users=fixture_json("sleeper/league_users.json"),
        rosters=fixture_json("sleeper/league_rosters.json"),
        transactions=[
            fixture_json("sleeper/transactions_completed_trade.json"),
            fixture_json("sleeper/transactions_add_drop.json"),
        ],
        traded_picks=[],
    )
    context = AppContext.create(settings=settings, sleeper_client=fake_client)
    context.crawl_service.discover()

    first_summary = context.crawl_service.sync_transactions()
    second_summary = context.crawl_service.sync_transactions()

    assert first_summary.status == "completed"
    assert first_summary.completed_trades_upserted == 1
    assert first_summary.add_drop_movements_upserted == 2
    assert second_summary.duplicates_skipped >= 2

    assert context.repositories.transactions.count() == 2
    assert context.repositories.trade_assets.count() == 3
    assert context.repositories.transaction_assets.count() == 2
    assert context.repositories.raw_payloads.count(source="sleeper") >= 2
