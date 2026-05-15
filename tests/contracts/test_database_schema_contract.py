from __future__ import annotations

import pytest


REQUIRED_TABLES = {
    "users",
    "leagues",
    "league_users",
    "rosters",
    "players",
    "raw_payloads",
    "transactions",
    "transaction_assets",
    "trade_sides",
    "trade_assets",
    "crawl_runs",
    "crawl_frontier",
    "fetched_markers",
    "league_sync_state",
    "ranking_runs",
    "ranking_assets",
    "ranking_evidence",
}

REQUIRED_COLUMNS = {
    "users": {
        "sleeper_user_id",
        "display_name",
        "raw_payload_json",
        "first_seen_at",
        "last_seen_at",
    },
    "leagues": {
        "sleeper_league_id",
        "season",
        "name",
        "total_rosters",
        "roster_positions_json",
        "settings_json",
        "scoring_settings_json",
        "raw_payload_json",
        "first_seen_at",
        "last_seen_at",
    },
    "league_users": {
        "sleeper_league_id",
        "sleeper_user_id",
        "roster_id",
        "display_name_at_fetch",
        "metadata_json",
    },
    "rosters": {
        "sleeper_league_id",
        "roster_id",
        "sleeper_user_id",
        "player_count",
        "starters_json",
        "players_json",
        "roster_value_context_json",
        "raw_payload_json",
    },
    "players": {
        "sleeper_player_id",
        "full_name",
        "position",
        "team",
        "metadata_json",
        "fetched_at",
    },
    "raw_payloads": {
        "id",
        "source",
        "endpoint",
        "external_id",
        "context_key",
        "content_hash",
        "payload_json",
        "fetched_at",
        "source_run_id",
    },
    "transactions": {
        "sleeper_transaction_id",
        "sleeper_league_id",
        "season",
        "type",
        "status",
        "created_at",
        "status_updated_at",
        "raw_payload_json",
    },
    "transaction_assets": {
        "id",
        "transaction_id",
        "league_id",
        "roster_id",
        "sleeper_user_id",
        "movement_kind",
        "asset_kind",
        "asset_key",
        "sleeper_player_id",
        "pick_season",
        "pick_round",
        "pick_original_roster_id",
        "pick_owner_roster_id",
        "pick_position",
        "raw_asset_json",
    },
    "trade_sides": {
        "id",
        "transaction_id",
        "league_id",
        "roster_id",
        "sleeper_user_id",
        "metadata_json",
    },
    "trade_assets": {
        "id",
        "trade_side_id",
        "asset_kind",
        "asset_key",
        "sleeper_player_id",
        "pick_season",
        "pick_round",
        "pick_original_roster_id",
        "pick_owner_roster_id",
        "pick_position",
        "raw_asset_json",
    },
    "crawl_runs": {
        "id",
        "run_type",
        "started_at",
        "finished_at",
        "status",
        "seed_username_hash_or_label",
        "season",
        "transaction_sync_since",
        "limits_json",
        "counts_json",
        "errors_json",
    },
    "crawl_frontier": {
        "id",
        "entity_type",
        "entity_id",
        "season",
        "status",
        "priority",
        "attempts",
        "last_error",
        "updated_at",
        "source_run_id",
    },
    "fetched_markers": {
        "entity_type",
        "entity_id",
        "season",
        "fetch_kind",
        "fetched_at",
        "high_watermark",
        "source_run_id",
    },
    "league_sync_state": {
        "sleeper_league_id",
        "season",
        "first_transaction_fetch_at",
        "last_transaction_fetch_at",
        "last_seen_transaction_timestamp",
        "last_seen_transaction_id",
        "transaction_backfill_complete",
        "updated_at",
    },
    "ranking_runs": {
        "id",
        "created_at",
        "season",
        "model_version",
        "config_json",
        "input_summary_json",
        "trade_count",
        "asset_count",
    },
    "ranking_assets": {
        "ranking_run_id",
        "asset_key",
        "rank",
        "asset_kind",
        "display_name",
        "position",
        "value_score",
        "confidence_label",
        "sample_count",
        "league_count",
        "recency_weight_sum",
        "direct_signal_count",
        "outlier_signal_count",
        "metadata_json",
    },
    "ranking_evidence": {
        "id",
        "ranking_run_id",
        "asset_key",
        "transaction_id",
        "league_id",
        "contribution_weight",
        "evidence_json",
    },
}

REQUIRED_UNIQUE_CONSTRAINT_COLUMNS = {
    "league_users": {"sleeper_league_id", "sleeper_user_id"},
    "rosters": {"sleeper_league_id", "roster_id"},
    "raw_payloads": {"source", "endpoint", "external_id", "context_key", "content_hash"},
    "transactions": {"sleeper_league_id", "sleeper_transaction_id"},
    "crawl_frontier": {"entity_type", "entity_id", "season"},
    "fetched_markers": {"entity_type", "entity_id", "season", "fetch_kind"},
    "league_sync_state": {"sleeper_league_id", "season"},
    "ranking_assets": {"ranking_run_id", "asset_key"},
}


@pytest.mark.contracts
def test_initial_database_schema_matches_architecture_contract(tmp_path) -> None:
    from sqlalchemy import create_engine, inspect

    from trade_winds.db.schema import create_database_schema

    engine = create_engine(f"sqlite:///{tmp_path / 'trade-winds.sqlite3'}")
    create_database_schema(engine)

    inspector = inspect(engine)

    table_names = set(inspector.get_table_names())
    assert REQUIRED_TABLES <= table_names

    for table_name, required_columns in REQUIRED_COLUMNS.items():
        actual_columns = {column["name"] for column in inspector.get_columns(table_name)}
        assert required_columns <= actual_columns, table_name

        primary_key = inspector.get_pk_constraint(table_name)["constrained_columns"]
        assert primary_key, f"{table_name} must have a primary key"

    for table_name, required_columns in REQUIRED_UNIQUE_CONSTRAINT_COLUMNS.items():
        unique_column_sets = [
            set(constraint["column_names"])
            for constraint in inspector.get_unique_constraints(table_name)
        ]
        primary_key_columns = set(inspector.get_pk_constraint(table_name)["constrained_columns"])

        assert (
            required_columns in unique_column_sets or required_columns <= primary_key_columns
        ), f"{table_name} must enforce idempotency on {sorted(required_columns)}"


@pytest.mark.contracts
def test_pick_precision_fields_are_nullable_for_unknown_exact_picks(tmp_path) -> None:
    from sqlalchemy import create_engine, inspect

    from trade_winds.db.schema import create_database_schema

    engine = create_engine(f"sqlite:///{tmp_path / 'trade-winds.sqlite3'}")
    create_database_schema(engine)
    inspector = inspect(engine)

    for table_name in ("transaction_assets", "trade_assets"):
        columns = {column["name"]: column for column in inspector.get_columns(table_name)}

        assert columns["pick_season"]["nullable"] is True
        assert columns["pick_round"]["nullable"] is True
        assert columns["pick_original_roster_id"]["nullable"] is True
        assert columns["pick_owner_roster_id"]["nullable"] is True
        assert columns["pick_position"]["nullable"] is True
