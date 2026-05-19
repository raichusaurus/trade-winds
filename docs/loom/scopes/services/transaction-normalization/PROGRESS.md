# Progress: Transaction Normalization

**Type:** Service  
**Parent:** [System Design Progress](../../system-design/PROGRESS.md)  
**Owner:** Codex + John Hightshue  
**Total Complete:** 67%  
**Current Focus:** Implement asset keys and transaction normalization  
**Last Updated:** 2026-05-18

## Navigation

- **Parent:** [System Design Progress](../../system-design/PROGRESS.md)
- **Project:** [Project Progress](../../../PROGRESS.md)
- **Implementation:** [Implementation Progress](../../../phases/implementation/PROGRESS.md)

## Phase Completion

| Phase | Complete | Weight | Evidence / Source | Notes |
|-------|----------|--------|-------------------|-------|
| Requirements | 100% | 1 | `docs/loom/02-requirements.md` | Completed trades, picks, and add/drops must be normalized. |
| Architecture | 100% | 1 | `docs/loom/03-architecture.md` | Asset identity and fact boundaries defined. |
| Planning & Decomposition | 100% | 1 | `docs/loom/04-planning.md` | Normalization precedes valuation. |
| Contracts & Tests | 100% | 1 | `tests/unit/test_asset_identity.py`; `tests/unit/test_transaction_normalizer_trades.py`; `tests/unit/test_transaction_normalizer_add_drop.py` | Identity and normalization contracts exist. |
| Implementation | 0% | 1 | `docs/loom/06-implementation.md` | Not implemented. |
| Review & Retrospective | 0% | 1 | `docs/loom/07-retrospective.md` | Not started. |
| **Phase Total** | **67%** | | | Ready for implementation. |

## Components

| Component | Requirements | Architecture | Planning | Contracts & Tests | Implementation | Review | Total | Notes |
|-----------|--------------|--------------|----------|-------------------|----------------|--------|-------|-------|
| Asset Identity | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Player/pick key contracts exist. |
| Trade Normalization | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Completed, exact-pick, multi-team, weird-trade contracts exist. |
| Add/Drop Normalization | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Baseline movement contract exists. |

## Smallest Tracked Units

| Unit | Parent Component | Contracts & Tests | Implementation | Review | Total | Evidence / Source |
|------|------------------|-------------------|----------------|--------|-------|-------------------|
| `player_asset_key` | Asset Identity | 100% | 0% | 0% | 33% | `tests/unit/test_asset_identity.py` |
| `pick_asset_key` | Asset Identity | 100% | 0% | 0% | 33% | `tests/unit/test_asset_identity.py` |
| `TransactionNormalizer` | Trade Normalization / Add-Drop Normalization | 100% | 0% | 0% | 33% | `tests/unit/test_transaction_normalizer_trades.py`; `tests/unit/test_transaction_normalizer_add_drop.py` |

## Next Score-Changing Actions

| Action | Phase / Area | Expected Score Impact | Owner |
|--------|--------------|-----------------------|-------|
| Implement asset key helpers | Implementation | Turns asset identity contracts green. | Codex |
| Implement transaction normalizer | Implementation | Turns trade/add-drop contracts green. | Codex |
