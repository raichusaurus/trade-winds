from __future__ import annotations

import pytest


@pytest.mark.integration
def test_ranking_generation_reads_persisted_facts_and_writes_evidence(tmp_path, fixture_json) -> None:
    from trade_winds.app import AppContext
    from trade_winds.config import Settings
    from trade_winds.testing.seed_data import seed_completed_trade_facts

    db_path = tmp_path / "trade-winds.sqlite3"
    seed_completed_trade_facts(
        database_path=db_path,
        league_id="league-1",
        transactions=[
            fixture_json("sleeper/transactions_completed_trade.json"),
            fixture_json("sleeper/transactions_weird_trade.json"),
        ],
    )
    context = AppContext.create(
        settings=Settings(
            sleeper_username="john_seed",
            season=2026,
            database_path=db_path,
            request_rate_per_second=1.0,
            max_users=10,
            max_leagues=5,
            max_api_calls=50,
            output_dir=tmp_path / "exports",
        )
    )

    summary = context.ranking_service.generate(model_version="trade-winds-v1")

    assert summary.status == "completed"
    assert summary.live_api_calls == 0
    assert summary.ranking_run_id
    assert summary.assets_ranked >= 3
    assert summary.evidence_rows_written >= 2

    rankings = context.ranking_query_service.rankings(run_id=summary.ranking_run_id)
    assert {row.asset_key for row in rankings.rows} >= {
        "player:4046",
        "player:7564",
        "pick:2027:1:2:unknown",
    }
    assert all(row.sample_count >= 1 for row in rankings.rows)
    assert all(row.confidence is not None for row in rankings.rows)
