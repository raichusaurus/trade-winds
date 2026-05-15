from __future__ import annotations

import pytest


@pytest.mark.contracts
def test_sleeper_fact_repository_upserts_users_leagues_and_rosters_idempotently(tmp_path) -> None:
    from trade_winds.db.testing import create_test_repository_bundle

    repositories = create_test_repository_bundle(tmp_path / "trade-winds.sqlite3")

    first = repositories.sleeper_facts.upsert_user(
        sleeper_user_id="user-1",
        username="original",
        display_name="Original Name",
        raw_payload={"user_id": "user-1", "username": "original"},
    )
    second = repositories.sleeper_facts.upsert_user(
        sleeper_user_id="user-1",
        username="renamed",
        display_name="Renamed User",
        raw_payload={"user_id": "user-1", "username": "renamed"},
    )

    assert first.created is True
    assert second.created is False
    assert repositories.users.count() == 1
    assert repositories.users.get("user-1").username == "renamed"

    repositories.sleeper_facts.upsert_league(
        sleeper_league_id="league-1",
        season=2026,
        name="Dynasty Test League",
        total_rosters=12,
        settings={"taxi_slots": 4},
        scoring_settings={"rec": 1.0},
        raw_payload={"league_id": "league-1"},
    )
    repositories.sleeper_facts.upsert_roster(
        sleeper_league_id="league-1",
        roster_id=1,
        sleeper_user_id="user-1",
        players=["4046"],
        starters=["4046"],
        raw_payload={"roster_id": 1},
    )
    repositories.sleeper_facts.upsert_roster(
        sleeper_league_id="league-1",
        roster_id=1,
        sleeper_user_id="user-1",
        players=["4046", "7564"],
        starters=["4046"],
        raw_payload={"roster_id": 1},
    )

    assert repositories.leagues.count() == 1
    assert repositories.rosters.count() == 1
    assert repositories.rosters.get("league-1", 1).player_count == 2


@pytest.mark.contracts
def test_crawl_state_repository_leases_completes_and_retries_frontier_items(tmp_path) -> None:
    from trade_winds.db.testing import create_test_repository_bundle

    repositories = create_test_repository_bundle(tmp_path / "trade-winds.sqlite3")
    crawl_run = repositories.crawl_state.start_run(
        run_type="discovery",
        season=2026,
        seed_username_hash_or_label="john_seed",
        limits={"max_users": 10},
    )

    repositories.crawl_state.enqueue_frontier(
        entity_type="user",
        entity_id="user-1",
        season=2026,
        priority=10,
        source_run_id=crawl_run.id,
    )
    repositories.crawl_state.enqueue_frontier(
        entity_type="user",
        entity_id="user-1",
        season=2026,
        priority=10,
        source_run_id=crawl_run.id,
    )

    leased = repositories.crawl_state.lease_next_frontier_item(season=2026)
    assert leased.entity_id == "user-1"
    assert repositories.crawl_state.frontier_count(status="in_progress") == 1
    assert repositories.crawl_state.frontier_count() == 1

    repositories.crawl_state.mark_frontier_failed(leased.id, "temporary failure")
    retry = repositories.crawl_state.lease_next_frontier_item(season=2026)
    assert retry.id == leased.id
    assert retry.attempts == 2

    repositories.crawl_state.mark_frontier_done(retry.id)
    assert repositories.crawl_state.frontier_count(status="done") == 1


@pytest.mark.contracts
def test_transaction_repository_upserts_raw_and_normalized_facts_idempotently(
    tmp_path,
    fixture_json,
) -> None:
    from trade_winds.db.testing import create_test_repository_bundle
    from trade_winds.transactions.normalizer import TransactionNormalizer

    repositories = create_test_repository_bundle(tmp_path / "trade-winds.sqlite3")
    payload = fixture_json("sleeper/transactions_completed_trade.json")
    normalized = TransactionNormalizer().normalize(
        transaction=payload,
        league_id="league-1",
        roster_context={"rosters": {"1": {"owner_id": "user-1"}, "2": {"owner_id": "user-2"}}},
        traded_picks=[],
    )

    first = repositories.transactions.upsert_normalized(normalized)
    second = repositories.transactions.upsert_normalized(normalized)

    assert first.created is True
    assert second.created is False
    assert repositories.transactions.count() == 1
    assert repositories.trade_sides.count(transaction_id="txn-trade-1") == 2
    assert repositories.trade_assets.count(transaction_id="txn-trade-1") == 3
    assert repositories.raw_payloads.count(source="sleeper") >= 1


@pytest.mark.contracts
def test_ranking_output_and_query_repositories_preserve_run_reproducibility(tmp_path) -> None:
    from trade_winds.db.testing import create_test_repository_bundle

    repositories = create_test_repository_bundle(tmp_path / "trade-winds.sqlite3")

    run = repositories.ranking_outputs.create_run(
        season=2026,
        model_version="trade-winds-v1",
        config={"recency_half_life_days": 90},
        input_summary={"completed_trade_count": 2},
    )
    repositories.ranking_outputs.replace_assets(
        run_id=run.id,
        assets=[
            {
                "asset_key": "player:4046",
                "rank": 1,
                "asset_kind": "player",
                "display_name": "Bijan Robinson",
                "position": "RB",
                "value_score": 100.0,
                "sample_count": 3,
            }
        ],
    )
    repositories.ranking_outputs.append_evidence(
        run_id=run.id,
        evidence=[
            {
                "asset_key": "player:4046",
                "transaction_id": "txn-trade-1",
                "league_id": "league-1",
                "contribution_weight": 0.75,
                "evidence": {"kind": "completed_trade"},
            }
        ],
    )

    queried_run = repositories.ranking_queries.get_run(run.id)
    rankings = repositories.ranking_queries.list_rankings(run_id=run.id)
    evidence = repositories.ranking_queries.asset_evidence(run_id=run.id, asset_key="player:4046")

    assert queried_run.model_version == "trade-winds-v1"
    assert queried_run.config["recency_half_life_days"] == 90
    assert rankings[0].asset_key == "player:4046"
    assert evidence[0].transaction_id == "txn-trade-1"
