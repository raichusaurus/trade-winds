from __future__ import annotations

import csv

import pytest


@pytest.mark.integration
def test_full_fixture_workflow_runs_discover_sync_rank_export_and_inspect(
    tmp_path,
    fixture_json,
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
        max_api_calls=50,
        output_dir=tmp_path / "exports",
    )
    context = AppContext.create(
        settings=settings,
        sleeper_client=FakeSleeperClient(
            seed_user=fixture_json("sleeper/user_seed.json"),
            leagues=fixture_json("sleeper/user_leagues_current_season.json"),
            league_users=fixture_json("sleeper/league_users.json"),
            rosters=fixture_json("sleeper/league_rosters.json"),
            transactions=[
                fixture_json("sleeper/transactions_completed_trade.json"),
                fixture_json("sleeper/transactions_add_drop.json"),
                fixture_json("sleeper/transactions_exact_pick_trade.json"),
            ],
            traded_picks=fixture_json("sleeper/traded_picks.json"),
            players=fixture_json("sleeper/players.json"),
        ),
    )

    crawl_summary = context.crawl_service.discover()
    sync_summary = context.crawl_service.sync_transactions()
    ranking_summary = context.ranking_service.generate(model_version="trade-winds-v1")
    export_summary = context.exporter.export_rankings(
        run_id=ranking_summary.ranking_run_id,
        output_path=tmp_path / "rankings.csv",
    )
    inspection = context.ranking_query_service.asset_evidence(
        run_id=ranking_summary.ranking_run_id,
        asset_key="player:4046",
    )

    assert crawl_summary.status == "completed"
    assert sync_summary.status == "completed"
    assert ranking_summary.status == "completed"
    assert export_summary.rows_written > 0
    assert inspection.rows

    rows = list(csv.DictReader((tmp_path / "rankings.csv").open(encoding="utf-8")))
    assert rows[0]["asset_key"]
    assert rows[0]["value_score"]
