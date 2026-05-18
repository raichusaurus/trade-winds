# Loom Progress Ledger

Project-specific completion ledger for Trade Winds. Update this document whenever changes are pushed to `main`, especially when a phase gate changes, implementation scope lands, tests move from red to green, or a workstream is added/removed.

## How Progress Is Scored

Percentages use the Loom defaults:

- `0%` = not started
- `25%` = drafted or started, major gaps remain
- `50%` = usable first pass, important gaps remain
- `75%` = mostly complete, known cleanup or validation remains
- `100%` = phase gate is satisfied for this scope
- `N/A` = phase does not apply and is excluded from calculations

Unless noted otherwise, phase weights are equal. Lower-level scopes inherit Requirements, Architecture, and Planning credit from the project phase docs when those docs define that scope clearly. Contract readiness is not the same as implemented product readiness: many units below are contract-ready but still have `0%` implementation because the `trade_winds` package has not been created yet.

## Project Snapshot

**Project:** trade-winds  
**Date:** 2026-05-18  
**Owner:** John Hightshue + Codex  
**Current Focus:** Implementation bootstrap after contract-ready Phase 5  
**Total Complete:** 70%  
**Calculation Basis:** Equal phase weights blended with equal-weight workstream child rollup

### Top-Level Phase Completion

| Phase | Complete | Weight | Evidence / Source | Notes |
|-------|----------|--------|-------------------|-------|
| Discovery | 100% | 1 | `docs/loom/01-discovery.md` | Phase gate closed. |
| Requirements | 100% | 1 | `docs/loom/02-requirements.md` | MVP scope and acceptance criteria documented. |
| Architecture | 100% | 1 | `docs/loom/03-architecture.md` | Component contracts and schema contract documented. |
| Planning & Decomposition | 100% | 1 | `docs/loom/04-planning.md` | Workstreams, slices, checkpoints, and handoffs documented. |
| Contracts & Tests | 100% | 1 | `docs/loom/05-contracts-tests-cicd.md`; `tests/` | Red executable contracts exist; live smoke skipped by default. |
| Implementation | 0% | 1 | `docs/loom/06-implementation.md` | `trade_winds` package scaffold not created yet. |
| Review & Retrospective | 0% | 1 | `docs/loom/07-retrospective.md` | Not started. |
| **Phase Total** | **71%** | | | Rounded from 500 / 700. |

### Top-Level Child Rollup

| Scope | Type | Weight | Phase Total | Child Rollup | Total | Owner | Notes |
|-------|------|--------|-------------|--------------|-------|-------|-------|
| Project Foundation | Workstream | 1 | 67% | 67% | 67% | Codex | Planned and tested; package scaffold still absent. |
| Service Boundary Design | Workstream | 1 | 67% | 67% | 67% | Codex | App context contracts exist; implementation absent. |
| Persistence & Schema | Workstream | 1 | 67% | 67% | 67% | Codex | Schema/repository/migration contracts exist. |
| Sleeper Client | Workstream | 1 | 67% | 67% | 67% | Codex | Endpoint, retry, rate-limit, fake-client contracts exist. |
| Crawl Orchestration | Workstream | 1 | 67% | 67% | 67% | Codex | Discovery and transaction sync contracts exist. |
| Transaction Normalization | Workstream | 1 | 67% | 67% | 67% | Codex | Trade/add-drop/pick/weird-trade contracts exist. |
| Valuation Engine | Workstream | 1 | 67% | 67% | 67% | Codex | Model, confidence, outlier, generation contracts exist. |
| Export & Inspection | Workstream | 1 | 67% | 67% | 67% | Codex | CSV, ranking, asset, compare contracts exist. |
| Tests & Contracts | Workstream | 1 | 83% | 83% | 83% | Codex | Phase 5 artifacts complete; review/retrospective remains. |
| CI Bootstrap | Workstream | 1 | 75% | 75% | 75% | Codex | Workflow exists for collection/Ruff; full pytest/type gates deferred. |
| **Child Rollup** | | | | | **69%** | | Rounded equal-weight average. |

## Workstream Progress

| Workstream | Requirements | Architecture | Planning | Contracts & Tests | Implementation | Review | Total | Evidence |
|------------|--------------|--------------|----------|-------------------|----------------|--------|-------|----------|
| Project Foundation | 100% | 100% | 100% | 100% | 0% | 0% | 67% | `tests/unit/test_settings.py`; `tests/cli/test_config_errors.py`; `tests/contracts/test_app_context_contract.py` |
| Service Boundary Design | 100% | 100% | 100% | 100% | 0% | 0% | 67% | `tests/contracts/test_app_context_contract.py`; `docs/loom/03-architecture.md#component-internal-contracts` |
| Persistence & Schema | 100% | 100% | 100% | 100% | 0% | 0% | 67% | `tests/contracts/test_database_schema_contract.py`; `tests/contracts/test_repository_contracts.py`; `tests/contracts/test_alembic_migrations_contract.py` |
| Sleeper Client | 100% | 100% | 100% | 100% | 0% | 0% | 67% | `tests/contracts/test_sleeper_client_contract.py`; `tests/unit/test_rate_limiter.py`; `tests/unit/test_retry_policy.py` |
| Crawl Orchestration | 100% | 100% | 100% | 100% | 0% | 0% | 67% | `tests/integration/test_crawl_discovery_resume.py`; `tests/integration/test_transaction_sync_persistence.py` |
| Transaction Normalization | 100% | 100% | 100% | 100% | 0% | 0% | 67% | `tests/unit/test_transaction_normalizer_trades.py`; `tests/unit/test_transaction_normalizer_add_drop.py`; `tests/unit/test_asset_identity.py` |
| Valuation Engine | 100% | 100% | 100% | 100% | 0% | 0% | 67% | `tests/unit/test_valuation_model_v1.py`; `tests/unit/test_confidence_and_outliers.py`; `tests/integration/test_ranking_generation.py` |
| Export & Inspection | 100% | 100% | 100% | 100% | 0% | 0% | 67% | `tests/cli/test_export_rankings.py`; `tests/cli/test_inspect_commands.py`; `tests/integration/test_ranking_comparison.py` |
| Tests & Contracts | 100% | 100% | 100% | 100% | 100% | 0% | 83% | `docs/loom/05-contracts-tests-cicd.md`; `docs/loom/05-remaining-needs.md`; `tests/` |
| CI Bootstrap | 100% | 100% | 100% | 100% | 50% | 0% | 75% | `.github/workflows/ci.yml`; `uv.lock`; `pyproject.toml`; full pytest promotion deferred. |

## Component Progress

| Component | Parent Workstream | Requirements | Architecture | Planning | Contracts & Tests | Implementation | Review | Total | Notes |
|-----------|-------------------|--------------|--------------|----------|-------------------|----------------|--------|-------|-------|
| Configuration | Project Foundation | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Env/default validation contract exists. |
| CLI Application | Project Foundation | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Command names/options are locked. |
| App Context | Service Boundary Design | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Wiring and override contracts exist. |
| Database Schema & Migrations | Persistence & Schema | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Table/key/raw JSON contracts exist. |
| Repository Bundle | Persistence & Schema | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Idempotency/query contracts exist. |
| Sleeper HTTP Client | Sleeper Client | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Endpoint/raw/error contracts exist. |
| Sleeper Resilience Helpers | Sleeper Client | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Retry/rate limiter contracts exist. |
| Sleeper Test Doubles | Sleeper Client | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Fake client/transport APIs accepted. |
| Discovery Crawl | Crawl Orchestration | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Resume/idempotency contract exists. |
| Transaction Sync | Crawl Orchestration | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Fixture sync persistence contract exists. |
| Asset Identity | Transaction Normalization | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Player/pick key contracts exist. |
| Trade Normalization | Transaction Normalization | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Completed, exact-pick, multi-team, weird-trade contracts exist. |
| Add/Drop Normalization | Transaction Normalization | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Baseline movement contract exists. |
| Ranking Model v1 | Valuation Engine | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Deterministic score and recency contracts exist. |
| Confidence & Outliers | Valuation Engine | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Context and lopsided-trade contracts exist. |
| Ranking Persistence & Generation | Valuation Engine | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Persisted-fact-only generation contract exists. |
| CSV Export | Export & Inspection | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Stable column contract exists. |
| Ranking Inspection | Export & Inspection | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Filter/evidence contracts exist. |
| Ranking Comparison | Export & Inspection | 100% | 100% | 100% | 100% | 0% | 0% | 67% | Run movement contract exists. |
| Fixture Workflow | Tests & Contracts | 100% | 100% | 100% | 100% | 100% | 0% | 83% | End-to-end fixture contract exists. |
| Check Automation | CI Bootstrap | 100% | 100% | 100% | 100% | 50% | 0% | 75% | Collection/Ruff CI exists; full pytest/type checks deferred. |

## Class / Unit Progress

Smallest tracked units are the classes, command groups, helpers, schemas, and workflows that currently have independent contracts or implementation ownership. Additional internal classes should be added here only when their completion matters independently.

| Class / Unit | Parent Component | Contracts & Tests | Implementation | Review | Total | Evidence / Source |
|--------------|------------------|-------------------|----------------|--------|-------|-------------------|
| `Settings` | Configuration | 100% | 0% | 0% | 33% | `tests/unit/test_settings.py` |
| `ConfigError` | Configuration | 100% | 0% | 0% | 33% | `tests/unit/test_settings.py`; `tests/cli/test_config_errors.py` |
| `trade_winds.cli.app` | CLI Application | 100% | 0% | 0% | 33% | `tests/cli/test_config_errors.py`; `tests/cli/test_command_options.py` |
| `crawl discover` command | CLI Application | 100% | 0% | 0% | 33% | `tests/cli/test_command_options.py` |
| `crawl transactions` command | CLI Application | 100% | 0% | 0% | 33% | `tests/cli/test_command_options.py` |
| `rank` command | CLI Application | 100% | 0% | 0% | 33% | `tests/cli/test_command_options.py` |
| `export rankings` command | CLI Application | 100% | 0% | 0% | 33% | `tests/cli/test_export_rankings.py` |
| `inspect rankings` command | CLI Application | 100% | 0% | 0% | 33% | `tests/cli/test_inspect_commands.py` |
| `inspect asset` command | CLI Application | 100% | 0% | 0% | 33% | `tests/cli/test_inspect_commands.py` |
| `inspect compare` command | CLI Application | 100% | 0% | 0% | 33% | `tests/cli/test_command_options.py`; `tests/integration/test_ranking_comparison.py` |
| `AppContext` | App Context | 100% | 0% | 0% | 33% | `tests/contracts/test_app_context_contract.py` |
| `create_database_schema` | Database Schema & Migrations | 100% | 0% | 0% | 33% | `tests/contracts/test_database_schema_contract.py` |
| `upgrade_to_head` / `downgrade_to_base` | Database Schema & Migrations | 100% | 0% | 0% | 33% | `tests/contracts/test_alembic_migrations_contract.py` |
| `create_test_repository_bundle` | Repository Bundle | 100% | 0% | 0% | 33% | `tests/contracts/test_repository_contracts.py` |
| User/league/roster repositories | Repository Bundle | 100% | 0% | 0% | 33% | `tests/contracts/test_repository_contracts.py` |
| Crawl state repository | Repository Bundle | 100% | 0% | 0% | 33% | `tests/contracts/test_repository_contracts.py` |
| Transaction repositories | Repository Bundle | 100% | 0% | 0% | 33% | `tests/contracts/test_repository_contracts.py` |
| Ranking repositories | Repository Bundle | 100% | 0% | 0% | 33% | `tests/contracts/test_repository_contracts.py` |
| `SleeperClient` | Sleeper HTTP Client | 100% | 0% | 0% | 33% | `tests/contracts/test_sleeper_client_contract.py` |
| `FakeSleeperTransport` | Sleeper Test Doubles | 100% | 0% | 0% | 33% | `tests/contracts/test_sleeper_client_contract.py` |
| `FakeSleeperClient` | Sleeper Test Doubles | 100% | 0% | 0% | 33% | `tests/integration/test_crawl_discovery_resume.py`; `tests/integration/test_full_fixture_workflow.py` |
| `RateLimiter` | Sleeper Resilience Helpers | 100% | 0% | 0% | 33% | `tests/unit/test_rate_limiter.py` |
| `FakeClock` | Sleeper Resilience Helpers | 100% | 0% | 0% | 33% | `tests/unit/test_rate_limiter.py` |
| `RetryPolicy` | Sleeper Resilience Helpers | 100% | 0% | 0% | 33% | `tests/unit/test_retry_policy.py` |
| Sleeper error classes | Sleeper Resilience Helpers | 100% | 0% | 0% | 33% | `tests/unit/test_retry_policy.py`; `tests/contracts/test_sleeper_client_contract.py` |
| `CrawlApplicationService.discover` | Discovery Crawl | 100% | 0% | 0% | 33% | `tests/integration/test_crawl_discovery_resume.py` |
| `CrawlApplicationService.sync_transactions` | Transaction Sync | 100% | 0% | 0% | 33% | `tests/integration/test_transaction_sync_persistence.py` |
| `player_asset_key` | Asset Identity | 100% | 0% | 0% | 33% | `tests/unit/test_asset_identity.py` |
| `pick_asset_key` | Asset Identity | 100% | 0% | 0% | 33% | `tests/unit/test_asset_identity.py` |
| `TransactionNormalizer` | Trade Normalization | 100% | 0% | 0% | 33% | `tests/unit/test_transaction_normalizer_trades.py`; `tests/unit/test_transaction_normalizer_add_drop.py` |
| `ValuationModelV1` | Ranking Model v1 | 100% | 0% | 0% | 33% | `tests/unit/test_valuation_model_v1.py` |
| `RankingConfig` | Ranking Model v1 | 100% | 0% | 0% | 33% | `tests/unit/test_valuation_model_v1.py` |
| `ConfidenceCalculator` | Confidence & Outliers | 100% | 0% | 0% | 33% | `tests/unit/test_confidence_and_outliers.py` |
| `OutlierDetector` | Confidence & Outliers | 100% | 0% | 0% | 33% | `tests/unit/test_confidence_and_outliers.py` |
| `RankingApplicationService.generate` | Ranking Persistence & Generation | 100% | 0% | 0% | 33% | `tests/integration/test_ranking_generation.py`; `tests/integration/test_full_fixture_workflow.py` |
| `RankingQueryService.rankings` | Ranking Inspection | 100% | 0% | 0% | 33% | `tests/cli/test_inspect_commands.py` |
| `RankingQueryService.asset_evidence` | Ranking Inspection | 100% | 0% | 0% | 33% | `tests/cli/test_inspect_commands.py`; `tests/integration/test_full_fixture_workflow.py` |
| `RankingQueryService.compare_runs` | Ranking Comparison | 100% | 0% | 0% | 33% | `tests/integration/test_ranking_comparison.py`; `tests/cli/test_command_options.py` |
| `CsvExporter.export_rankings` | CSV Export | 100% | 0% | 0% | 33% | `tests/cli/test_export_rankings.py`; `tests/integration/test_full_fixture_workflow.py` |
| `seed_ranking_run` | Fixture Workflow | 100% | 0% | 0% | 33% | `tests/cli/test_export_rankings.py`; `tests/cli/test_inspect_commands.py`; `tests/integration/test_ranking_comparison.py` |
| `seed_completed_trade_facts` | Fixture Workflow | 100% | 0% | 0% | 33% | `tests/integration/test_ranking_generation.py` |
| GitHub Actions contract-readiness workflow | Check Automation | 100% | 50% | 0% | 50% | `.github/workflows/ci.yml`; `docs/loom/05-contracts-tests-cicd.md#check-automation-handoff` |

## Decisions and Adjustments

| Date | Scope | Change | Reason | Owner |
|------|-------|--------|--------|-------|
| 2026-05-18 | Project | Added recursive progress ledger | Loom framework now expects percent complete by project, workstream, component, and smallest tracked unit. | Codex |
| 2026-05-18 | Contracts & Tests | Counted Phase 5 as 100% contract-ready | Missing CLI command contracts were added and remaining needs are implementation-facing. | Codex |
| 2026-05-18 | CI Bootstrap | Counted CI as 50% implemented inside its workstream | Collection/Ruff workflow exists; full pytest, coverage, type checking, and migration gates are deferred until implementation can pass them. | Codex |

## Open Progress Questions

| Scope | Question | Needed To Score Accurately | Owner |
|-------|----------|----------------------------|-------|
| Type checking | Pyright or mypy? | Decide before scoring type-check automation beyond deferred. | John + Codex |
| HTTP mocking | `pytest-httpx` or `respx`? | Decide during Sleeper client implementation if fixture transport is not enough. | Codex |
| Scope weights | Should MVP delivery weight persistence/crawl/valuation more heavily than docs/governance? | Current rollup uses equal weights; adjust if delivery progress should dominate. | John |
| CI/CD phase shape | Should CI/CD become a standalone Loom phase/checkpoint? | Current project treats it as a bootstrap workstream; framework question remains open. | John |
