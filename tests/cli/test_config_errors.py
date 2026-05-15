from __future__ import annotations

from typer.testing import CliRunner


def test_cli_help_renders_registered_commands() -> None:
    from trade_winds.cli import app

    result = CliRunner().invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "crawl" in result.output
    assert "rank" in result.output
    assert "export" in result.output
    assert "inspect" in result.output


def test_crawl_discover_reports_missing_seed_username(monkeypatch) -> None:
    from trade_winds.cli import app

    monkeypatch.delenv("TRADE_WINDS_SLEEPER_USERNAME", raising=False)
    monkeypatch.setenv("TRADE_WINDS_DB_PATH", ":memory:")

    result = CliRunner().invoke(app, ["crawl", "discover"])

    assert result.exit_code != 0
    assert "TRADE_WINDS_SLEEPER_USERNAME" in result.output
    assert "seed Sleeper username" in result.output
