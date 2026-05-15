from __future__ import annotations

from typer.testing import CliRunner


def test_crawl_discover_accepts_limit_and_rate_overrides(monkeypatch, tmp_path) -> None:
    from trade_winds.cli import app
    from trade_winds.testing.cli import install_fake_app_context

    fake_context = install_fake_app_context()
    monkeypatch.setenv("TRADE_WINDS_SLEEPER_USERNAME", "john_seed")
    monkeypatch.setenv("TRADE_WINDS_DB_PATH", str(tmp_path / "trade-winds.sqlite3"))

    result = CliRunner().invoke(
        app,
        [
            "crawl",
            "discover",
            "--max-users",
            "3",
            "--max-leagues",
            "2",
            "--max-api-calls",
            "10",
            "--request-rate",
            "1.5",
        ],
    )

    assert result.exit_code == 0
    assert fake_context.crawl_service.discover_calls[0].max_users == 3
    assert fake_context.crawl_service.discover_calls[0].max_leagues == 2
    assert fake_context.crawl_service.discover_calls[0].max_api_calls == 10
    assert fake_context.crawl_service.discover_calls[0].request_rate_per_second == 1.5


def test_rank_accepts_model_version_and_run_label(monkeypatch, tmp_path) -> None:
    from trade_winds.cli import app
    from trade_winds.testing.cli import install_fake_app_context

    fake_context = install_fake_app_context()
    monkeypatch.setenv("TRADE_WINDS_SLEEPER_USERNAME", "john_seed")
    monkeypatch.setenv("TRADE_WINDS_DB_PATH", str(tmp_path / "trade-winds.sqlite3"))

    result = CliRunner().invoke(
        app,
        ["rank", "--model-version", "trade-winds-v1", "--run-label", "smoke"],
    )

    assert result.exit_code == 0
    assert fake_context.ranking_service.generate_calls[0].model_version == "trade-winds-v1"
    assert fake_context.ranking_service.generate_calls[0].run_label == "smoke"


def test_inspect_compare_requires_two_run_ids(monkeypatch, tmp_path) -> None:
    from trade_winds.cli import app

    monkeypatch.setenv("TRADE_WINDS_SLEEPER_USERNAME", "john_seed")
    monkeypatch.setenv("TRADE_WINDS_DB_PATH", str(tmp_path / "trade-winds.sqlite3"))

    result = CliRunner().invoke(app, ["inspect", "compare", "--from-run", "run-a"])

    assert result.exit_code != 0
    assert "--to-run" in result.output
