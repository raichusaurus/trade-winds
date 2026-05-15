from __future__ import annotations


def test_valuation_model_v1_scores_deterministically_from_fixture_input(fixture_json) -> None:
    from trade_winds.valuation.model_v1 import RankingConfig, ValuationModelV1
    from trade_winds.valuation.testing import ranking_input_from_fixture

    ranking_input = ranking_input_from_fixture(fixture_json("rankings/model_v1_minimal_input.json"))
    config = RankingConfig(model_version="trade-winds-v1", recency_half_life_days=90)

    result = ValuationModelV1().score(ranking_input, config)

    assert result.model_version == "trade-winds-v1"
    assert [asset.asset_key for asset in result.assets] == [
        "player:4046",
        "player:7564",
        "pick:2027:1:2:unknown",
        "player:1111",
    ]
    assert [asset.value_score for asset in result.assets] == [100.0, 94.0, 62.0, 1.0]
    assert result.assets[0].confidence.sample_count == 2
    assert result.assets[-1].confidence.add_drop_baseline_count == 2


def test_valuation_model_v1_applies_recency_weighting(fixture_json) -> None:
    from trade_winds.valuation.model_v1 import RankingConfig, ValuationModelV1
    from trade_winds.valuation.testing import ranking_input_from_fixture

    ranking_input = ranking_input_from_fixture(fixture_json("rankings/model_v1_recency_input.json"))

    fast_decay = ValuationModelV1().score(
        ranking_input,
        RankingConfig(model_version="trade-winds-v1", recency_half_life_days=30),
    )
    slow_decay = ValuationModelV1().score(
        ranking_input,
        RankingConfig(model_version="trade-winds-v1", recency_half_life_days=180),
    )

    assert fast_decay.asset_by_key("player:4046").value_score > fast_decay.asset_by_key(
        "player:7564"
    ).value_score
    assert slow_decay.asset_by_key("player:4046").value_score < fast_decay.asset_by_key(
        "player:4046"
    ).value_score
