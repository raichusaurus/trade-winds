# Progress: System Design

**Type:** Scope  
**Parent:** [Project Progress](../../PROGRESS.md)  
**Owner:** Codex + John Hightshue  
**Total Complete:** 67%  
**Current Focus:** Track the designed service/component/unit hierarchy through implementation  
**Last Updated:** 2026-05-18

## Navigation

- **Parent:** [Project Progress](../../PROGRESS.md)
- **Contracts drilldown:** [Contracts & Tests Progress](../../phases/contracts-tests/PROGRESS.md)
- **Implementation drilldown:** [Implementation Progress](../../phases/implementation/PROGRESS.md)
- **Architecture:** [Architecture](../../03-architecture.md)
- **Planning:** [Planning & Decomposition](../../04-planning.md)

## Phase Completion

| Phase | Complete | Weight | Evidence / Source | Notes |
|-------|----------|--------|-------------------|-------|
| Requirements | 100% | 1 | `docs/loom/02-requirements.md` | MVP scope defines the system boundary. |
| Architecture | 100% | 1 | `docs/loom/03-architecture.md` | Services, components, data contracts, and CLI surfaces are designed. |
| Planning & Decomposition | 100% | 1 | `docs/loom/04-planning.md` | Workstreams and ownership boundaries are decomposed. |
| Contracts & Tests | 100% | 1 | `docs/loom/05-contracts-tests-cicd.md`; `tests/` | Each service/component area has executable contracts. |
| Implementation | 0% | 1 | `docs/loom/06-implementation.md` | Production package does not exist yet. |
| Review & Retrospective | 0% | 1 | `docs/loom/07-retrospective.md` | Not started. |
| **Phase Total** | **67%** | | | Design and contracts are complete; implementation is next. |

## Services

For this local-first MVP, "service" means an owned implementation boundary or application service area, not a separately deployed process.

| Service | Weight | Phase Total | Child Rollup | Total | Progress Doc | Notes |
|---------|--------|-------------|--------------|-------|--------------|-------|
| Project Foundation | 1 | 67% | 67% | 67% | [Implementation Progress](../../phases/implementation/PROGRESS.md) | Config, CLI shell, package scaffold. |
| Service Boundary Design | 1 | 67% | 67% | 67% | [Implementation Progress](../../phases/implementation/PROGRESS.md) | App context and application services. |
| Persistence & Schema | 1 | 67% | 67% | 67% | [Implementation Progress](../../phases/implementation/PROGRESS.md) | SQLite schema, migrations, repositories. |
| Sleeper Client | 1 | 67% | 67% | 67% | [Implementation Progress](../../phases/implementation/PROGRESS.md) | API client, resilience, test doubles. |
| Crawl Orchestration | 1 | 67% | 67% | 67% | [Implementation Progress](../../phases/implementation/PROGRESS.md) | Discovery and transaction sync. |
| Transaction Normalization | 1 | 67% | 67% | 67% | [Implementation Progress](../../phases/implementation/PROGRESS.md) | Asset identity, trade/add-drop normalization. |
| Valuation Engine | 1 | 67% | 67% | 67% | [Implementation Progress](../../phases/implementation/PROGRESS.md) | Model, confidence, outliers, ranking generation. |
| Export & Inspection | 1 | 67% | 67% | 67% | [Implementation Progress](../../phases/implementation/PROGRESS.md) | CSV export and query/CLI inspection. |
| **Child Rollup** | | | | **67%** | | Equal-weight average. |

## Components

| Component | Parent Service | Requirements | Architecture | Planning | Contracts & Tests | Implementation | Review | Total | Notes |
|-----------|----------------|--------------|--------------|----------|-------------------|----------------|--------|-------|-------|
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

## Smallest Tracked Units

These are the smallest classes, command groups, helpers, schemas, and workflows currently worth tracking independently. Add internal units only when their completion status matters on its own.

| Unit | Parent Component | Contracts & Tests | Implementation | Review | Total | Evidence / Source |
|------|------------------|-------------------|----------------|--------|-------|-------------------|
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
| Create `trade_winds` package scaffold | Implementation / system design | Moves implementation above 0% for foundation units. | Codex |
| Split a service/component into its own child progress doc | Progress organization | Improves navigation if a scope develops independent blockers or ownership. | Codex |

## Blockers and Questions

| Item | Impact | Owner | Next Step |
|------|--------|-------|-----------|
| Production modules not created | All system-design units remain 0% implementation. | Codex | Start implementation bootstrap. |
| Scope weights are equal by default | May understate/overstate heavy persistence/crawl/valuation work. | John | Decide whether to weight services by effort or risk later. |
