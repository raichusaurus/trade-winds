from __future__ import annotations

from typer.testing import CliRunner


def test_inspect_rankings_filters_by_asset_type_and_position(monkeypatch, tmp_path) -> None:
    from trade_winds.cli import app
    from trade_winds.testing.seed_data import seed_ranking_run

    db_path = tmp_path / "trade-winds.sqlite3"
    seed_ranking_run(
        database_path=db_path,
        run_id="rank-run-1",
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
            },
            {
                "rank": 2,
                "asset_key": "pick:2027:1:unknown:unknown",
                "asset_type": "pick",
                "name": "2027 Round 1 Pick",
                "position": None,
                "value_score": 86.0,
                "sample_count": 2,
                "confidence": 0.48,
            },
        ],
    )
    monkeypatch.setenv("TRADE_WINDS_SLEEPER_USERNAME", "john_seed")
    monkeypatch.setenv("TRADE_WINDS_DB_PATH", str(db_path))

    result = CliRunner().invoke(
        app,
        ["inspect", "rankings", "--run-id", "rank-run-1", "--asset-type", "player", "--position", "RB"],
    )

    assert result.exit_code == 0
    assert "Bijan Robinson" in result.output
    assert "player:4046" in result.output
    assert "2027 Round 1 Pick" not in result.output


def test_inspect_asset_shows_source_trade_evidence(monkeypatch, tmp_path) -> None:
    from trade_winds.cli import app
    from trade_winds.testing.seed_data import seed_ranking_run

    db_path = tmp_path / "trade-winds.sqlite3"
    seed_ranking_run(
        database_path=db_path,
        run_id="rank-run-1",
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
        evidence=[
            {
                "asset_key": "player:4046",
                "transaction_id": "txn-trade-1",
                "contribution": 0.61,
                "is_outlier": False,
                "notes": "Recent completed trade",
            }
        ],
    )
    monkeypatch.setenv("TRADE_WINDS_SLEEPER_USERNAME", "john_seed")
    monkeypatch.setenv("TRADE_WINDS_DB_PATH", str(db_path))

    result = CliRunner().invoke(
        app,
        ["inspect", "asset", "player:4046", "--run-id", "rank-run-1"],
    )

    assert result.exit_code == 0
    assert "Bijan Robinson" in result.output
    assert "txn-trade-1" in result.output
    assert "Recent completed trade" in result.output
