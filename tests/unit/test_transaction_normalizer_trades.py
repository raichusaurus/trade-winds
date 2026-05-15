from __future__ import annotations


def test_normalizer_captures_completed_trade_sides_assets_and_raw_reference(fixture_json) -> None:
    from trade_winds.transactions.normalizer import TransactionNormalizer

    payload = fixture_json("sleeper/transactions_completed_trade.json")

    normalized = TransactionNormalizer().normalize(
        transaction=payload,
        league_id="league-1",
        roster_context={"rosters": {"1": {"owner_id": "user-1"}, "2": {"owner_id": "user-2"}}},
        traded_picks=[],
    )

    assert normalized.transaction.transaction_id == "txn-trade-1"
    assert normalized.transaction.league_id == "league-1"
    assert normalized.transaction.status == "complete"
    assert normalized.transaction.transaction_type == "trade"
    assert normalized.transaction.raw_payload == payload

    assert [side.roster_id for side in normalized.trade_sides] == ["1", "2"]
    assert {asset.asset_key for asset in normalized.trade_assets} == {
        "player:4046",
        "player:7564",
        "pick:2027:1:2:unknown",
    }


def test_normalizer_preserves_weird_completed_trades_for_outlier_review(fixture_json) -> None:
    from trade_winds.transactions.normalizer import TransactionNormalizer

    payload = fixture_json("sleeper/transactions_weird_trade.json")

    normalized = TransactionNormalizer().normalize(
        transaction=payload,
        league_id="league-1",
        roster_context={"rosters": {"1": {"owner_id": "user-1"}, "2": {"owner_id": "user-2"}}},
        traded_picks=[],
    )

    assert normalized.transaction.transaction_id == "txn-weird-trade-1"
    assert normalized.transaction.status == "complete"
    assert normalized.transaction.is_outlier_candidate is True
    assert normalized.trade_assets != []


def test_normalizer_captures_multiteam_trade_sides(fixture_json) -> None:
    from trade_winds.transactions.normalizer import TransactionNormalizer

    payload = fixture_json("sleeper/transactions_multiteam_trade.json")

    normalized = TransactionNormalizer().normalize(
        transaction=payload,
        league_id="league-1",
        roster_context={
            "rosters": {
                "1": {"owner_id": "user-1"},
                "2": {"owner_id": "user-2"},
                "3": {"owner_id": "user-3"},
            }
        },
        traded_picks=[],
    )

    assert [side.roster_id for side in normalized.trade_sides] == ["1", "2", "3"]
    assert {asset.asset_key for asset in normalized.trade_assets} == {
        "player:4046",
        "player:7564",
        "player:9999",
    }


def test_normalizer_preserves_exact_pick_position_when_known(fixture_json) -> None:
    from trade_winds.transactions.normalizer import TransactionNormalizer

    payload = fixture_json("sleeper/transactions_exact_pick_trade.json")

    normalized = TransactionNormalizer().normalize(
        transaction=payload,
        league_id="league-1",
        roster_context={"rosters": {"1": {"owner_id": "user-1"}, "2": {"owner_id": "user-2"}}},
        traded_picks=fixture_json("sleeper/traded_picks.json"),
    )

    pick_assets = [asset for asset in normalized.trade_assets if asset.asset_kind == "pick"]

    assert pick_assets[0].asset_key == "pick:2027:1:2:3"
    assert pick_assets[0].pick_position == 3


def test_normalizer_records_warning_for_missing_roster_context(fixture_json) -> None:
    from trade_winds.transactions.normalizer import TransactionNormalizer

    payload = fixture_json("sleeper/transactions_completed_trade.json")

    normalized = TransactionNormalizer().normalize(
        transaction=payload,
        league_id="league-1",
        roster_context={"rosters": {}},
        traded_picks=[],
    )

    assert "missing_roster_context" in normalized.warnings
    assert normalized.transaction.raw_payload == payload
