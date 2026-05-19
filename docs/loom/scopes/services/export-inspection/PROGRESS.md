# Progress: Export & Inspection

**Type:** Service  
**Parent:** [System Design Progress](../../system-design/PROGRESS.md)  
**Owner:** Codex + John Hightshue  
**Total Complete:** 67%  
**Current Focus:** Implement CSV export and ranking inspection/query surfaces  
**Last Updated:** 2026-05-18

## Navigation

- **Parent:** [System Design Progress](../../system-design/PROGRESS.md)
- **Project:** [Project Progress](../../../PROGRESS.md)
- **Implementation:** [Implementation Progress](../../../phases/implementation/PROGRESS.md)

## Phase Completion

| Phase | Complete | Weight | Evidence / Source | Notes |
|-------|----------|--------|-------------------|-------|
| Requirements | 100% | 1 | `docs/loom/02-requirements.md` | CSV and inspection surfaces required for MVP validation. |
| Architecture | 100% | 1 | `docs/loom/03-architecture.md` | Export/query boundaries defined. |
| Planning & Decomposition | 100% | 1 | `docs/loom/04-planning.md` | Export/inspection follows ranking persistence. |
| Contracts & Tests | 100% | 1 | `tests/cli/test_export_rankings.py`; `tests/cli/test_inspect_commands.py`; `tests/integration/test_ranking_comparison.py` | Export and inspection contracts exist. |
| Implementation | 0% | 1 | `docs/loom/06-implementation.md` | Not implemented. |
| Review & Retrospective | 0% | 1 | `docs/loom/07-retrospective.md` | Not started. |
| **Phase Total** | **67%** | | | Ready for implementation. |

## Components

| Component | Requirements | Architecture | Planning | Contracts & Tests | Implementation | Review | Total | Notes |
|-----------|--------------|--------------|----------|-------------------|----------------|--------|-------|-------|
| CSV Export | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Stable column contract exists. |
| Ranking Inspection | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Filter/evidence contracts exist. |
| Ranking Comparison | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Run movement contract exists. |

## Smallest Tracked Units

| Unit | Parent Component | Contracts & Tests | Implementation | Review | Total | Evidence / Source |
|------|------------------|-------------------|----------------|--------|-------|-------------------|
| `CsvExporter.export_rankings` | CSV Export | 100% | 0% | 0% | 33% | `tests/cli/test_export_rankings.py`; `tests/integration/test_full_fixture_workflow.py` |
| `RankingQueryService.rankings` | Ranking Inspection | 100% | 0% | 0% | 33% | `tests/cli/test_inspect_commands.py` |
| `RankingQueryService.asset_evidence` | Ranking Inspection | 100% | 0% | 0% | 33% | `tests/cli/test_inspect_commands.py`; `tests/integration/test_full_fixture_workflow.py` |
| `RankingQueryService.compare_runs` | Ranking Comparison | 100% | 0% | 0% | 33% | `tests/integration/test_ranking_comparison.py`; `tests/cli/test_command_options.py` |
| `seed_ranking_run` | Test Support | 100% | 0% | 0% | 33% | `tests/cli/test_export_rankings.py`; `tests/cli/test_inspect_commands.py`; `tests/integration/test_ranking_comparison.py` |
| `seed_completed_trade_facts` | Test Support | 100% | 0% | 0% | 33% | `tests/integration/test_ranking_generation.py` |

## Next Score-Changing Actions

| Action | Phase / Area | Expected Score Impact | Owner |
|--------|--------------|-----------------------|-------|
| Implement CSV exporter | Implementation | Turns export contract green. | Codex |
| Implement ranking query service | Implementation | Turns inspection/comparison contracts green. | Codex |
