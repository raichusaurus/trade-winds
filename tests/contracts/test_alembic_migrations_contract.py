from __future__ import annotations

import pytest


@pytest.mark.contracts
def test_alembic_upgrade_head_creates_schema_contract_tables(tmp_path) -> None:
    from sqlalchemy import create_engine, inspect

    from trade_winds.db.migrations import upgrade_to_head

    engine = create_engine(f"sqlite:///{tmp_path / 'trade-winds.sqlite3'}")

    upgrade_to_head(engine)

    table_names = set(inspect(engine).get_table_names())
    assert {
        "users",
        "leagues",
        "transactions",
        "crawl_runs",
        "ranking_runs",
        "ranking_assets",
        "ranking_evidence",
    } <= table_names


@pytest.mark.contracts
def test_alembic_downgrade_base_removes_application_tables(tmp_path) -> None:
    from sqlalchemy import create_engine, inspect

    from trade_winds.db.migrations import downgrade_to_base, upgrade_to_head

    engine = create_engine(f"sqlite:///{tmp_path / 'trade-winds.sqlite3'}")
    upgrade_to_head(engine)

    downgrade_to_base(engine)

    assert inspect(engine).get_table_names() == []
