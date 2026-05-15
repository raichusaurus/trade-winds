from __future__ import annotations


def test_app_context_wires_settings_session_factory_repositories_and_services(tmp_path) -> None:
    from trade_winds.app import AppContext
    from trade_winds.config import Settings

    settings = Settings(
        sleeper_username="seed-user",
        season=2026,
        database_path=tmp_path / "trade-winds.sqlite3",
        request_rate_per_second=1.0,
        max_users=10,
        max_leagues=5,
        max_api_calls=50,
        output_dir=tmp_path / "exports",
    )

    context = AppContext.create(settings=settings)

    assert context.settings == settings
    assert context.session_factory is not None
    assert context.repositories is not None
    assert context.sleeper_client is not None
    assert context.crawl_service is not None
    assert context.ranking_service is not None
    assert context.exporter is not None
    assert context.ranking_query_service is not None


def test_app_context_accepts_test_dependency_overrides(tmp_path) -> None:
    from trade_winds.app import AppContext
    from trade_winds.config import Settings

    class FakeSleeperClient:
        pass

    settings = Settings(
        sleeper_username="seed-user",
        season=2026,
        database_path=tmp_path / "trade-winds.sqlite3",
        request_rate_per_second=1.0,
        max_users=10,
        max_leagues=5,
        max_api_calls=50,
        output_dir=tmp_path / "exports",
    )
    fake_client = FakeSleeperClient()

    context = AppContext.create(settings=settings, sleeper_client=fake_client)

    assert context.sleeper_client is fake_client
