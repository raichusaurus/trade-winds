# Progress: Implementation

**Type:** Phase  
**Parent:** [Project Progress](../../PROGRESS.md)  
**Owner:** Codex + John Hightshue  
**Total Complete:** 0% implementation, 67% contract/planning readiness across delivery workstreams  
**Current Focus:** Create the `trade_winds` package scaffold and keep pytest collection green  
**Last Updated:** 2026-05-18

## Navigation

- **Parent:** [Project Progress](../../PROGRESS.md)
- **Related phase doc:** [Implementation](../../06-implementation.md)
- **Planning:** [Planning & Decomposition](../../04-planning.md)
- **Contracts:** [Contracts & Tests / CI/CD](../../05-contracts-tests-cicd.md)

## Phase Completion

| Phase | Complete | Weight | Evidence / Source | Notes |
|-------|----------|--------|-------------------|-------|
| Requirements | 100% | 1 | `docs/loom/02-requirements.md` | MVP scope and acceptance criteria define implementation target. |
| Architecture | 100% | 1 | `docs/loom/03-architecture.md` | Component boundaries and data contracts defined. |
| Planning & Decomposition | 100% | 1 | `docs/loom/04-planning.md` | Workstreams, slices, and handoffs defined. |
| Contracts & Tests | 100% | 1 | `docs/loom/05-contracts-tests-cicd.md`; `tests/` | 58 tests collect; full suite intentionally red. |
| Implementation | 0% | 1 | `docs/loom/06-implementation.md` | `trade_winds` package does not exist yet. |
| Review & Retrospective | 0% | 1 | `docs/loom/07-retrospective.md` | Not started. |
| **Phase Total** | **67%** | | | Ready for implementation, not implemented. |

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

## Next Score-Changing Actions

| Action | Phase / Area | Expected Score Impact | Owner |
|--------|--------------|-----------------------|-------|
| Create the minimal `trade_winds` package scaffold and keep collection green | Implementation / Project Foundation | Moves Project Foundation implementation above 0%; may increase project total if scaffold is accepted as implementation progress. | Codex |
| Implement settings/env validation and CLI help/config errors | Implementation / Project Foundation | Turns first focused red contracts green for Configuration and CLI Application units. | Codex |
| Implement `AppContext.create` dependency wiring and test override path | Implementation / Service Boundary Design | Moves App Context implementation above 0%. | Codex |
| Implement database schema creation and migration helpers | Implementation / Persistence & Schema | Moves schema/migration units above 0% and unlocks repository work. | Codex |

## Blockers and Questions

| Item | Impact | Owner | Next Step |
|------|--------|-------|-----------|
| No `trade_winds` package | Full pytest fails at import time. | Codex | Create package scaffold first. |
| Type checker undecided | Type-check implementation cannot be scored yet. | John + Codex | Decide Pyright or mypy during scaffold slice. |
| HTTP mocking library undecided | Sleeper client test-support shape may change. | Codex | Decide during Sleeper client slice if fake transport is insufficient. |
