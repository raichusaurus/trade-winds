# Progress: Crawl Orchestration

**Type:** Service  
**Parent:** [System Design Progress](../../system-design/PROGRESS.md)  
**Owner:** Codex + John Hightshue  
**Total Complete:** 67%  
**Current Focus:** Implement discovery and transaction sync application services  
**Last Updated:** 2026-05-18

## Navigation

- **Parent:** [System Design Progress](../../system-design/PROGRESS.md)
- **Project:** [Project Progress](../../../PROGRESS.md)
- **Implementation:** [Implementation Progress](../../../phases/implementation/PROGRESS.md)

## Phase Completion

| Phase | Complete | Weight | Evidence / Source | Notes |
|-------|----------|--------|-------------------|-------|
| Requirements | 100% | 1 | `docs/loom/02-requirements.md` | Resumable crawl and transaction sync required. |
| Architecture | 100% | 1 | `docs/loom/03-architecture.md` | Frontier/fetched-marker design defined. |
| Planning & Decomposition | 100% | 1 | `docs/loom/04-planning.md` | Crawl follows persistence and client foundation. |
| Contracts & Tests | 100% | 1 | `tests/integration/test_crawl_discovery_resume.py`; `tests/integration/test_transaction_sync_persistence.py` | Resume and sync contracts exist. |
| Implementation | 0% | 1 | `docs/loom/06-implementation.md` | Not implemented. |
| Review & Retrospective | 0% | 1 | `docs/loom/07-retrospective.md` | Not started. |
| **Phase Total** | **67%** | | | Ready for implementation. |

## Components

| Component | Requirements | Architecture | Planning | Contracts & Tests | Implementation | Review | Total | Notes |
|-----------|--------------|--------------|----------|-------------------|----------------|--------|-------|-------|
| Discovery Crawl | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Resume/idempotency contract exists. |
| Transaction Sync | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Fixture sync persistence contract exists. |

## Smallest Tracked Units

| Unit | Parent Component | Contracts & Tests | Implementation | Review | Total | Evidence / Source |
|------|------------------|-------------------|----------------|--------|-------|-------------------|
| `CrawlApplicationService.discover` | Discovery Crawl | 100% | 0% | 0% | 33% | `tests/integration/test_crawl_discovery_resume.py` |
| `CrawlApplicationService.sync_transactions` | Transaction Sync | 100% | 0% | 0% | 33% | `tests/integration/test_transaction_sync_persistence.py` |

## Next Score-Changing Actions

| Action | Phase / Area | Expected Score Impact | Owner |
|--------|--------------|-----------------------|-------|
| Implement discovery orchestration | Implementation | Moves discovery implementation above 0%. | Codex |
| Implement transaction sync | Implementation | Moves transaction sync implementation above 0%. | Codex |
