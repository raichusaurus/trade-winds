from __future__ import annotations

import csv

from typer.testing import CliRunner


def test_export_rankings_writes_stable_csv_columns(monkeypatch, tmp_path) -> None:
    from trade_winds.cli import app
    from trade_winds.testing.seed_data import seed_ranking_run

    db_path = tmp_path / "trade-winds.sqlite3"
    output_path = tmp_path / "rankings.csv"
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
    )
    monkeypatch.setenv("TRADE_WINDS_SLEEPER_USERNAME", "john_seed")
    monkeypatch.setenv("TRADE_WINDS_DB_PATH", str(db_path))

    result = CliRunner().invoke(
        app,
        ["export", "rankings", "--run-id", "rank-run-1", "--output", str(output_path)],
    )

    assert result.exit_code == 0
    assert "1 ranking rows" in result.output
    assert output_path.exists()

    rows = list(csv.DictReader(output_path.open(encoding="utf-8")))
    assert rows == [
        {
            "run_id": "rank-run-1",
            "rank": "1",
            "asset_key": "player:4046",
            "asset_type": "player",
            "name": "Bijan Robinson",
            "position": "RB",
            "pick_season": "",
            "pick_round": "",
            "value_score": "100.0",
            "sample_count": "4",
            "confidence": "0.72",
        }
    ]
