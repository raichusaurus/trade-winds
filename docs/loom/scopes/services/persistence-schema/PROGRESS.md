# Progress: Persistence & Schema

**Type:** Service  
**Parent:** [System Design Progress](../../system-design/PROGRESS.md)  
**Owner:** Codex + John Hightshue  
**Total Complete:** 67%  
**Current Focus:** Implement SQLite schema, migrations, and repository bundle  
**Last Updated:** 2026-05-18

## Navigation

- **Parent:** [System Design Progress](../../system-design/PROGRESS.md)
- **Project:** [Project Progress](../../../PROGRESS.md)
- **Implementation:** [Implementation Progress](../../../phases/implementation/PROGRESS.md)

## Phase Completion

| Phase | Complete | Weight | Evidence / Source | Notes |
|-------|----------|--------|-------------------|-------|
| Requirements | 100% | 1 | `docs/loom/02-requirements.md` | Durable local persistence required. |
| Architecture | 100% | 1 | `docs/loom/03-architecture.md` | Schema contract defined. |
| Planning & Decomposition | 100% | 1 | `docs/loom/04-planning.md` | Persistence blocks crawl/ranking storage. |
| Contracts & Tests | 100% | 1 | `tests/contracts/test_database_schema_contract.py`; `tests/contracts/test_repository_contracts.py` | Schema and repository behavior covered. |
| Implementation | 0% | 1 | `docs/loom/06-implementation.md` | Not implemented. |
| Review & Retrospective | 0% | 1 | `docs/loom/07-retrospective.md` | Not started. |
| **Phase Total** | **67%** | | | Ready for implementation. |

## Components

| Component | Requirements | Architecture | Planning | Contracts & Tests | Implementation | Review | Total | Notes |
|-----------|--------------|--------------|----------|-------------------|----------------|--------|-------|-------|
| Database Schema & Migrations | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Table/key/raw JSON contracts exist. |
| Repository Bundle | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Idempotency/query contracts exist. |

## Smallest Tracked Units

| Unit | Parent Component | Contracts & Tests | Implementation | Review | Total | Evidence / Source |
|------|------------------|-------------------|----------------|--------|-------|-------------------|
| `create_database_schema` | Database Schema & Migrations | 100% | 0% | 0% | 33% | `tests/contracts/test_database_schema_contract.py` |
| `upgrade_to_head` / `downgrade_to_base` | Database Schema & Migrations | 100% | 0% | 0% | 33% | `tests/contracts/test_alembic_migrations_contract.py` |
| `create_test_repository_bundle` | Repository Bundle | 100% | 0% | 0% | 33% | `tests/contracts/test_repository_contracts.py` |
| User/league/roster repositories | Repository Bundle | 100% | 0% | 0% | 33% | `tests/contracts/test_repository_contracts.py` |
| Crawl state repository | Repository Bundle | 100% | 0% | 0% | 33% | `tests/contracts/test_repository_contracts.py` |
| Transaction repositories | Repository Bundle | 100% | 0% | 0% | 33% | `tests/contracts/test_repository_contracts.py` |
| Ranking repositories | Repository Bundle | 100% | 0% | 0% | 33% | `tests/contracts/test_repository_contracts.py` |

## Next Score-Changing Actions

| Action | Phase / Area | Expected Score Impact | Owner |
|--------|--------------|-----------------------|-------|
| Implement schema creation | Implementation | Moves schema implementation above 0%. | Codex |
| Implement repository bundle | Implementation | Unlocks crawl/ranking persistence work. | Codex |
