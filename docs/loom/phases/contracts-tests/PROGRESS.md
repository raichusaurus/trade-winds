# Progress: Contracts & Tests

**Type:** Phase  
**Parent:** [Project Progress](../../PROGRESS.md)  
**Owner:** Codex + John Hightshue  
**Total Complete:** 100% for contract readiness  
**Current Focus:** Preserve locked contracts while implementation turns them green  
**Last Updated:** 2026-05-18

## Navigation

- **Parent:** [Project Progress](../../PROGRESS.md)
- **Related phase doc:** [Contracts & Tests / CI/CD](../../05-contracts-tests-cicd.md)
- **Implementation handoff:** [Phase 5 Remaining Needs](../../05-remaining-needs.md)

## Phase Completion

| Phase | Complete | Weight | Evidence / Source | Notes |
|-------|----------|--------|-------------------|-------|
| Requirements | 100% | 1 | `docs/loom/02-requirements.md` | MVP behavior is testable. |
| Architecture | 100% | 1 | `docs/loom/03-architecture.md` | Component and schema contracts defined. |
| Planning & Decomposition | 100% | 1 | `docs/loom/04-planning.md` | Contract/test candidates carried forward. |
| Contracts & Tests | 100% | 1 | `docs/loom/05-contracts-tests-cicd.md`; `tests/` | Executable red contracts exist. |
| Implementation | 100% | 1 | `tests/`; `.github/workflows/ci.yml` | Test/CI artifacts are implemented; production code is tracked under Implementation. |
| Review & Retrospective | 0% | 1 | `docs/loom/07-retrospective.md` | Not started. |
| **Phase Total** | **83%** | | | Phase itself is complete; retrospective remains. |

## Test Readiness Matrix

| Area | Status | Evidence | Notes |
|------|--------|----------|-------|
| Settings/env validation | Covered | `tests/unit/test_settings.py`; `tests/cli/test_config_errors.py` | Locked. |
| App context wiring | Covered | `tests/contracts/test_app_context_contract.py` | Locked with approved API-shape rewrite only. |
| CLI command/options | Covered | `tests/cli/test_command_options.py`; `tests/cli/test_export_rankings.py`; `tests/cli/test_inspect_commands.py` | Covers discovery, transaction sync, rank, export, inspect, compare. |
| Schema and migrations | Covered | `tests/contracts/test_database_schema_contract.py`; `tests/contracts/test_alembic_migrations_contract.py` | Locked. |
| Repository contracts | Covered | `tests/contracts/test_repository_contracts.py` | Idempotency and deterministic queries. |
| Sleeper client endpoints | Covered | `tests/contracts/test_sleeper_client_contract.py` | Raw payloads, retries, not-found behavior. |
| Rate limiting/retry policy | Covered | `tests/unit/test_rate_limiter.py`; `tests/unit/test_retry_policy.py` | Fake clock and bounded retry contracts. |
| Crawl workflow | Covered | `tests/integration/test_crawl_discovery_resume.py`; `tests/integration/test_transaction_sync_persistence.py` | Resume and idempotent sync. |
| Transaction normalization | Covered | `tests/unit/test_transaction_normalizer_trades.py`; `tests/unit/test_transaction_normalizer_add_drop.py`; `tests/unit/test_asset_identity.py` | Trades, picks, add/drop, warnings. |
| Valuation/confidence/outliers | Covered | `tests/unit/test_valuation_model_v1.py`; `tests/unit/test_confidence_and_outliers.py` | Exact model fixture currently approval-required before rewrite. |
| Export/inspection/comparison | Covered | `tests/cli/test_export_rankings.py`; `tests/cli/test_inspect_commands.py`; `tests/integration/test_ranking_comparison.py` | Stable CSV and query surfaces. |
| Full fixture workflow | Covered | `tests/integration/test_full_fixture_workflow.py` | End-to-end local fixture path. |
| Live Sleeper smoke | Covered, opt-in | `tests/live/test_sleeper_live_smoke.py` | Skipped by default. |
| Type checking | Deferred | `docs/loom/05-contracts-tests-cicd.md` | Choose Pyright or mypy during scaffold slice. |

## Automation Status

| Check | Current Status | Blocking? | Next Change |
|-------|----------------|-----------|-------------|
| `uv sync --locked` | Implemented in CI | Yes | Keep locked. |
| `ruff format --check .` | Implemented in CI | Yes | Keep locked. |
| `ruff check .` | Implemented in CI | Yes | Keep locked. |
| `pytest --collect-only` | Implemented in CI | Yes | Replace or supplement with full pytest once implementation can pass. |
| Full `pytest` | Deferred | No | Promote after implementation slices are green. |
| Coverage | Deferred | No | Start informational after first stable green suite. |
| Type checking | Deferred | No | Choose Pyright or mypy first. |
| Live Sleeper smoke | Manual/opt-in | No | Never make normal PR gate. |

## Children

| Scope | Type | Weight | Total | Progress Doc | Notes |
|-------|------|--------|-------|--------------|-------|
| CI Bootstrap | Workstream | 1 | 75% | This document | Contract-readiness workflow exists; full pytest/type/coverage deferred. |
| Test Suite | Workstream | 1 | 83% | This document | Contracts are implemented; retrospective not started. |

## Next Score-Changing Actions

| Action | Phase / Area | Expected Score Impact | Owner |
|--------|--------------|-----------------------|-------|
| Choose Pyright or mypy | CI Bootstrap | Moves type-checking from deferred to planned or implemented. | John + Codex |
| Promote CI to full pytest | CI Bootstrap | Moves automation implementation above 50% after production code passes. | Codex |
| Add coverage reporting | CI Bootstrap | Improves quality-gate completeness after green suite stabilizes. | Codex |

## Blockers and Questions

| Item | Impact | Owner | Next Step |
|------|--------|-------|-----------|
| Type checker choice | Blocks type-check CI scoring. | John + Codex | Decide during scaffold slice. |
| Full pytest intentionally red | Prevents full-test CI gate. | Codex | Implement production code slice by slice. |
