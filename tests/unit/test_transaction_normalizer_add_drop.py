from __future__ import annotations


def test_normalizer_captures_add_drop_assets_without_trade_sides(fixture_json) -> None:
    from trade_winds.transactions.normalizer import TransactionNormalizer

    payload = fixture_json("sleeper/transactions_add_drop.json")

    normalized = TransactionNormalizer().normalize(
        transaction=payload,
        league_id="league-1",
        roster_context={"league_size": 12, "roster_size": 28},
        traded_picks=[],
    )

    assert normalized.transaction.transaction_id == "txn-add-drop-1"
    assert normalized.transaction.transaction_type == "waiver"
    assert normalized.trade_sides == []
    assert {asset.asset_key for asset in normalized.transaction_assets} == {
        "player:1111",
        "player:2222",
    }
    assert {asset.direction for asset in normalized.transaction_assets} == {"add", "drop"}
    assert normalized.transaction_assets_by_key["player:1111"].baseline_eligible is True
    assert normalized.transaction_assets_by_key["player:2222"].baseline_eligible is True
