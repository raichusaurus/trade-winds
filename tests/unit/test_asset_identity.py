from __future__ import annotations


def test_player_asset_key_uses_sleeper_player_id() -> None:
    from trade_winds.assets import player_asset_key

    assert player_asset_key("4046") == "player:4046"


def test_pick_asset_key_uses_unknown_literals_for_missing_precision() -> None:
    from trade_winds.assets import pick_asset_key

    assert (
        pick_asset_key(season=2027, round=1, original_owner=None, pick_number=None)
        == "pick:2027:1:unknown:unknown"
    )


def test_pick_asset_key_is_deterministic_for_known_pick() -> None:
    from trade_winds.assets import pick_asset_key

    assert (
        pick_asset_key(season=2027, round=2, original_owner="roster-7", pick_number=18)
        == "pick:2027:2:roster-7:18"
    )
