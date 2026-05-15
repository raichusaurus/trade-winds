from __future__ import annotations

import pytest


@pytest.mark.integration
def test_ranking_query_service_compares_asset_movement_between_runs(tmp_path) -> None:
    from trade_winds.app import AppContext
    from trade_winds.config import Settings
    from trade_winds.testing.seed_data import seed_ranking_run

    db_path = tmp_path / "trade-winds.sqlite3"
    seed_ranking_run(
        database_path=db_path,
        run_id="rank-run-older",
        assets=[
            {
                "rank": 5,
                "asset_key": "player:4046",
                "asset_type": "player",
                "name": "Bijan Robinson",
                "position": "RB",
                "value_score": 89.0,
                "sample_count": 2,
                "confidence": 0.45,
            }
        ],
    )
    seed_ranking_run(
        database_path=db_path,
        run_id="rank-run-newer",
        assets=[
            {
                "rank": 1,
                "asset_key": "player:4046",
                "asset_type": "player",
                "name": "Bijan Robinson",
                "position": "RB",
                "value_score": 100.0,
                "sample_count": 4,
                "confidence": 0.72,
            }
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

    comparison = context.ranking_query_service.compare_runs(
        from_run_id="rank-run-older",
        to_run_id="rank-run-newer",
    )

    assert comparison.rows[0].asset_key == "player:4046"
    assert comparison.rows[0].rank_delta == -4
    assert comparison.rows[0].value_score_delta == 11.0
    assert comparison.rows[0].is_unstable is True
