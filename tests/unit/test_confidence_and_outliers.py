from __future__ import annotations


def test_confidence_calculator_exposes_sample_league_recency_and_outlier_context() -> None:
    from trade_winds.valuation.confidence import ConfidenceCalculator
    from trade_winds.valuation.types import EvidenceContribution

    confidence = ConfidenceCalculator().calculate(
        asset_key="player:4046",
        evidence=[
            EvidenceContribution(
                asset_key="player:4046",
                transaction_id="txn-1",
                league_id="league-1",
                recency_weight=1.0,
                is_direct_signal=True,
                is_outlier=False,
            ),
            EvidenceContribution(
                asset_key="player:4046",
                transaction_id="txn-2",
                league_id="league-2",
                recency_weight=0.5,
                is_direct_signal=False,
                is_outlier=True,
            ),
        ],
    )

    assert confidence.sample_count == 2
    assert confidence.league_count == 2
    assert confidence.recency_weight_sum == 1.5
    assert confidence.direct_signal_count == 1
    assert confidence.outlier_signal_count == 1
    assert confidence.label in {"low", "medium", "high"}


def test_outlier_detector_flags_lopsided_completed_trade_without_dropping_it() -> None:
    from trade_winds.valuation.outliers import OutlierDetector
    from trade_winds.valuation.types import TradeConstraint

    trade = TradeConstraint(
        transaction_id="txn-weird-trade-1",
        league_id="league-1",
        side_asset_keys={
            "1": ["player:4046", "player:7564", "player:9999"],
            "2": ["player:1111"],
        },
        created_at=None,
    )

    result = OutlierDetector(max_asset_count_ratio=2.0).evaluate(trade)

    assert result.is_outlier is True
    assert result.transaction_id == "txn-weird-trade-1"
    assert result.should_preserve_fact is True
