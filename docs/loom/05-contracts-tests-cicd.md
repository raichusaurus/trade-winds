# Contracts & Tests / CI/CD

Define how Trade Winds will be verified before implementation begins.

**Project Name:** trade-winds  
**Date:** 2026-05-15  
**Test/CI Lead:** Codex + John Hightshue

---

## Inputs

- Requirements document: `docs/loom/02-requirements.md`
- Architecture document: `docs/loom/03-architecture.md`
- Planning & Decomposition document: `docs/loom/04-planning.md`
- Architecture component/internal contracts: `docs/loom/03-architecture.md#component-internal-contracts`
- Planning contract/test candidates: `docs/loom/04-planning.md#contract--test-candidates`

---

## Testing Decision

Trade Winds will use test-first development for the MVP.

Implementation work cannot begin for a service, component, class, repository, CLI command, or persistence contract until its intended behavior is represented by failing tests or executable contract checks. Project scaffolding may create empty modules, interfaces, dataclasses, and command shells only when needed to make tests importable and runnable.

Existing contract tests should be treated as implementation requirements. During implementation, new tests may be added freely when new behavior, edge cases, defects, or real Sleeper payloads are discovered. Existing tests should not be rewritten to fit a convenient implementation.

An existing test may be rewritten only when John explicitly approves the rewrite after the implementation owner explains:

- Why the current test is mechanically invalid, contradictory, or impossible to satisfy without violating a higher-level requirement.
- Whether the issue is with the behavior contract, the test-support API, fixture assumptions, or the expected output.
- What implementation was attempted or considered before asking to change the test.
- The smallest proposed test change.
- Which requirement, architecture decision, or planning contract remains protected after the rewrite.

The minimum loop is:

1. Write or update the contract/test that describes the next behavior.
2. Run the focused test and confirm it fails for the expected reason.
3. Implement the smallest production change needed to pass.
4. Run the focused test plus the relevant surrounding suite.
5. Refactor only while the tests stay green.

No network-dependent test is required for normal local development or CI. Sleeper API behavior must be covered with recorded or handcrafted fixture payloads. Live API smoke tests are opt-in only.

### Contract Stability Register

This register tells the implementation session how strongly to treat current tests as locked. "Locked" means code should be shaped to satisfy the test. "Approval required before rewrite" means the test is still a contract, but it contains test-support API or model-detail assumptions that may need a deliberate, approved adjustment if implementation proves the shape wrong.

| Test Area | Stability | Notes |
|-----------|-----------|-------|
| Settings/env validation | Locked | Config key names, defaults, and validation should be implemented as tested unless requirements change. |
| Asset identity | Locked | Asset keys are shared across normalization, valuation, export, and inspection. Rewriting requires architecture approval. |
| Schema contract | Locked | Tables, raw JSON columns, uniqueness/idempotency keys, and nullable pick precision are implementation requirements. |
| Sleeper endpoint behavior | Locked | Endpoint methods, raw payload retention, retry/not-found behavior, and parsed response fields should be implemented as tested. |
| Transaction normalization behavior | Locked with fixture expansion allowed | Existing trade/add/drop/pick/weird-trade behavior is locked. Add fixtures for new Sleeper edge cases rather than rewriting old ones unless contradictory. |
| CLI command names and core options | Locked | Command names and core operator options should stay stable. Add option tests as commands grow. |
| Repository behavior | Approval required before rewrite | Idempotency and query behavior are locked, but exact test-support bundle shape such as `create_test_repository_bundle` can be adjusted only with approval if implementation chooses a cleaner equivalent. |
| App context composition | Approval required before rewrite | Dependency wiring is locked. Attribute names may need approval if a cleaner composition object preserves the same boundary. |
| Test doubles and seed helpers | Approval required before rewrite | `FakeSleeperClient`, `FakeSleeperTransport`, `install_fake_app_context`, `seed_ranking_run`, and `seed_completed_trade_facts` are accepted test-support APIs, but may be refined with approval if they block clean implementation. |
| Valuation model v1 exact scores | Approval required before rewrite | The deterministic fixture outputs are the current model-v1 contract. If implementation shows the numbers are mathematically inconsistent with the chosen explainable algorithm, explain and request approval before changing them. |
| Full fixture workflow | Approval required before rewrite | The workflow order is locked. Exact helper/service return shapes may require approved adjustment if a cleaner API preserves the behavior. |
| Live Sleeper smoke test | Flexible/non-blocking | This test is opt-in and may be adjusted to match live API realities without changing core MVP behavior. |
| CI/CD workflow | Deferred | CI checks are planned but not yet implemented. Once `.github/workflows/ci.yml` exists, rewrites follow the same approval rule. |

### Accepted Test-Support APIs

Implementation may create helper modules under `trade_winds.testing` and similar test-support namespaces to satisfy contracts without leaking testing concerns into production services.

Accepted test-support APIs:

| API | Purpose |
|-----|---------|
| `trade_winds.db.testing.create_test_repository_bundle` | Create a migrated temp database and repository bundle for repository contract tests. |
| `trade_winds.sleeper.testing.FakeSleeperClient` | Provide deterministic fixture-backed Sleeper responses for crawl/integration tests. |
| `trade_winds.sleeper.testing.FakeSleeperTransport` | Provide deterministic route-level responses for Sleeper client contract tests. |
| `trade_winds.testing.seed_data.seed_ranking_run` | Seed persisted ranking outputs for export/inspection tests. |
| `trade_winds.testing.seed_data.seed_completed_trade_facts` | Seed normalized persisted trade facts for ranking tests. |
| `trade_winds.testing.cli.install_fake_app_context` | Install a fake application context for CLI option/dispatch tests. |
| `trade_winds.valuation.testing.ranking_input_from_fixture` | Convert stable ranking JSON fixtures into model input DTOs. |

These helpers are allowed because they make tests readable and keep production services focused. If an implementation session wants to rename, remove, or substantially reshape one of these helpers, it must use the rewrite approval process above.

---

## Framework Recommendation

### Primary Test Stack

| Tool | Use | Recommendation |
|------|-----|----------------|
| `pytest` | Unit, integration, contract, CLI, and regression tests | Use as the primary test runner. It has strong fixture, parametrization, temporary path, monkeypatch, and plugin support. |
| `pytest-cov` | Coverage reporting | Use in CI after the first implementation slice. Coverage gates should start modestly and rise as modules stabilize. |
| `typer.testing.CliRunner` | CLI command tests | Use for command smoke tests and CLI behavior contracts. |
| `pytest-httpx` or `respx` | Mocking `httpx` calls | Use one HTTP mocking library for Sleeper client tests. Prefer `pytest-httpx` if the client stays simple; use `respx` if route-level matching becomes clearer. |
| `tmp_path` fixtures | Isolated SQLite databases, exports, config files | Use per-test temporary directories instead of shared local data paths. |
| `monkeypatch` fixtures | Environment variables and time/config overrides | Use for config loading and deterministic CLI/service behavior. |
| `Hypothesis` | Property-based tests for normalization and ranking invariants | Add selectively after example-based behavior is clear. Do not use it as a substitute for readable examples. |
| `Ruff` | Linting and formatting | Use for fast lint and format checks in CI. |
| `Pyright` or `mypy` | Static type checks | Defer the choice until package scaffolding. Prefer Pyright if editor/type feedback is the priority; prefer mypy if SQLAlchemy plugin support becomes important. |

### Why `pytest`

`pytest` should be the default because it gives us concise tests, reusable fixtures, parametrized cases, temporary filesystem support, environment monkeypatching, and a large plugin ecosystem without forcing a heavy class-based style. That fits this project better than Python's built-in `unittest`, especially because Trade Winds will need many small service and repository fixtures.

Recommended pattern:

```text
tests/
  unit/
  integration/
  contracts/
  cli/
  fixtures/
    sleeper/
    rankings/
```

Test file naming:

```text
test_<component>_<behavior>.py
```

Examples:

```text
tests/contracts/test_sleeper_client_contract.py
tests/unit/test_transaction_normalizer_trades.py
tests/integration/test_crawl_discovery_resume.py
tests/cli/test_rank_command.py
```

---

## Test Categories

| Category | Purpose | Speed | External Dependencies | Required in CI |
|----------|---------|-------|------------------------|----------------|
| Unit tests | Verify pure functions, classes, models, parsing, scoring, and small service branches | Fast | None | Yes |
| Component contract tests | Lock public behavior at each service/repository/client boundary | Fast to medium | None | Yes |
| Persistence integration tests | Verify SQLite schema, migrations, repositories, idempotent upserts, and query behavior | Medium | Local SQLite only | Yes |
| CLI tests | Verify command names, option contracts, clear errors, and summaries | Fast to medium | None | Yes |
| Fixture-based Sleeper tests | Verify API parsing and normalization from representative payloads | Fast | None | Yes |
| End-to-end local workflow tests | Run crawl/rank/export/inspect services against fixtures and temp DB | Medium | None | Yes |
| Live Sleeper smoke tests | Verify real API compatibility with a configured seed username | Slow/variable | Sleeper API | No, opt-in only |
| Property-based tests | Probe invariants in normalization, asset identities, and ranking math | Variable | None | Yes when stable |

---

## Contracts & Interfaces

### API / Service Contracts

| Contract | Owner | Consumers | Inputs | Outputs | Error Cases |
|----------|-------|-----------|--------|---------|-------------|
| `Settings.load()` | Configuration | CLI, `AppContext` | Environment variables, ignored local config, defaults | Typed settings with seed username, season, DB path, rate limits, crawl limits, output paths | Missing seed username; invalid season; invalid rate/limit; unwritable configured paths |
| `AppContext.create()` | Application foundation | CLI, future API adapter | Settings and optional dependency overrides | Wired settings, session factory, repositories, Sleeper client, services | Database path invalid; migration/session setup failure; dependency misconfiguration |
| `SleeperClient.get_user_by_username()` | Sleeper Client | Crawl discovery | Username | Parsed user payload plus raw JSON | 404/not found; malformed payload; transient HTTP failure; rate-limit response |
| `SleeperClient.get_user_leagues()` | Sleeper Client | Crawl discovery | User ID, season | League payloads plus raw JSON | Empty league list; malformed payload; transient HTTP failure |
| `SleeperClient.get_league_users()` | Sleeper Client | Crawl discovery | League ID | League user payloads plus raw JSON | League not found; malformed payload; transient HTTP failure |
| `SleeperClient.get_league_rosters()` | Sleeper Client | Crawl discovery, baseline context | League ID | Roster payloads plus raw JSON | League not found; malformed roster settings |
| `SleeperClient.get_league_transactions()` | Sleeper Client | Transaction sync | League ID, round/week if needed | Transaction payloads plus raw JSON | Empty week; malformed transaction; transient HTTP failure |
| `SleeperClient.get_traded_picks()` | Sleeper Client | Transaction sync | League ID | Draft-pick movement payloads plus raw JSON | Missing pick fields; malformed payload |
| `CrawlApplicationService.discover()` | Crawl | CLI, future API adapter | Settings, seed username, limits, repositories, Sleeper client | `CrawlSummary` with counts, status, errors, limit flags | Missing config; seed not found; max limits reached; interrupted run; retry exhaustion |
| `CrawlApplicationService.sync_transactions()` | Crawl | CLI, future API adapter | Known leagues, season, sync state, Sleeper client | `TransactionSyncSummary` with transaction/add/drop/trade counts | No known leagues; malformed transaction; partial failure; retry exhaustion |
| `TransactionNormalizer.normalize()` | Normalization | Transaction sync, tests, future model work | Raw Sleeper transaction, league/roster context, traded picks | Normalized transaction facts, trade sides, trade assets, add/drop assets, raw reference | Unknown transaction type; missing roster/user; unknown player; unknown pick precision |
| `RankingApplicationService.generate()` | Valuation | CLI, future API adapter | Ranking config, persisted transaction facts | `RankingSummary`, persisted ranking run/assets/evidence | No eligible trades; sparse data; invalid model config; persistence failure |
| `ValuationModel.score()` | Valuation | Ranking service | Completed trade facts, add/drop baseline facts, model config | Asset scores, confidence metrics, outlier signals, evidence contributions | Contradictory assets; insufficient connected graph; invalid weights |
| `RankingQueryService` | Inspection | CLI, export, future API adapter | Run ID/latest selector, filters, asset key | Ranking rows, run metadata, evidence rows, comparison rows | Run not found; asset not found; invalid filter |
| `CsvExporter.export_rankings()` | Export | CLI, validation workflow | Run ID/latest selector, destination path, filters | CSV file with stable columns and row count summary | Run not found; path unwritable; unsupported filter |
| CLI commands | CLI | Operator | Command names/options/env | Exit code, stdout/stderr, created artifacts | Missing config; invalid option; no data; command failure with readable message |

### Class / Component Contracts

Every production class must have a test file that covers its public behavior before class implementation starts.

| Component/Class | Required Test Focus |
|-----------------|---------------------|
| Settings model | Defaults, env overrides, validation, local path behavior |
| App context | Dependency wiring, test overrides, CLI-safe error messages |
| Rate limiter | Sleeps or virtual-time delays between requests; honors configured rate |
| Retry policy | Retries transient failures with bounded attempts; does not retry permanent failures |
| Sleeper endpoint models | Permissive parsing, raw payload retention, stable IDs |
| Repository classes | Idempotent upserts, transactions, uniqueness, query filters |
| Crawl frontier manager | Lease, complete, retry, resume, and limit behavior |
| Fetched marker manager | Prevents duplicate fetch work without hiding failed work |
| Transaction normalizer | Trade sides/assets, add/drop facts, draft picks, odd trades, raw references |
| Asset identity helper | Stable keys for players and picks; reversible enough for inspection |
| Valuation model v1 | Recency weighting, trade-equivalence constraints, baseline calibration hooks, confidence metrics |
| Outlier detector | Flags unusual trades without deleting raw facts |
| Ranking writer | Creates reproducible runs/assets/evidence with model metadata |
| Query services | Filters, latest-run behavior, asset evidence drilldown, movement comparison |
| CSV exporter | Stable columns, deterministic ordering, safe overwrite behavior |
| CLI renderers | Concise summaries, useful errors, no raw stack traces for expected failures |

### CLI / UI / Workflow Contracts

| Surface | Contract | Required Evidence |
|---------|----------|-------------------|
| `trade-winds --help` | Renders primary command groups without requiring config | `tests/cli/test_config_errors.py` |
| `trade-winds crawl discover` | Loads config, accepts crawl/rate limits, calls crawl discovery service, reports missing seed username clearly | `tests/cli/test_config_errors.py`, `tests/cli/test_command_options.py` |
| `trade-winds crawl transactions` | Reads known leagues and syncs transactions through crawl application service | `tests/integration/test_transaction_sync_persistence.py`; add command-specific CLI test during implementation |
| `trade-winds rank` | Generates persisted ranking run from persisted facts only; accepts model version/run label | `tests/integration/test_ranking_generation.py`, `tests/cli/test_command_options.py` |
| `trade-winds export rankings` | Writes stable ranking CSV columns from persisted ranking run | `tests/cli/test_export_rankings.py` |
| `trade-winds inspect rankings` | Reads persisted ranking rows and supports asset type/position filters | `tests/cli/test_inspect_commands.py` |
| `trade-winds inspect asset <asset_key>` | Shows asset ranking context and source evidence | `tests/cli/test_inspect_commands.py` |
| `trade-winds inspect compare` | Requires two run IDs and compares rank/value movement | `tests/cli/test_command_options.py`, `tests/integration/test_ranking_comparison.py` |
| Fixture workflow | Discover, sync, rank, export, and inspect complete without live Sleeper calls | `tests/integration/test_full_fixture_workflow.py` |

---

## Data Contracts

### Database / Model Contracts

| Schema/Event/Model | Owner | Fields | Compatibility Notes |
|--------------------|-------|--------|---------------------|
| `users` | Persistence | Sleeper user ID, username/display name fields, raw snapshot, timestamps | Upsert by Sleeper user ID; usernames may change |
| `leagues` | Persistence | League ID, season, name, settings JSON, scoring/settings snapshots, timestamps | Upsert by league ID; preserve raw settings |
| `league_users` | Persistence | League ID, user ID, roster/user metadata, timestamps | Many-to-many; idempotent |
| `rosters` | Persistence | League ID, roster ID, owner user ID, players, starters, taxi/IR/context JSON | Preserve enough context for add/drop baseline |
| `crawl_runs` | Persistence/Crawl | Run ID, type, status, started/finished timestamps, counts, errors, limits | Required for resumability and operator summaries |
| `crawl_frontier` | Persistence/Crawl | Frontier item ID, item type, external ID, priority/depth, status, attempts, leased timestamp | Must allow interrupted work to be retried |
| `fetched_markers` | Persistence/Crawl | Fetch key, type, external ID, season/week/context, status, fetched timestamp | Prevents duplicate calls while distinguishing failures |
| `league_sync_state` | Persistence/Crawl | League ID, season, last synced scope/week, status, error | Transactions can resume per league |
| `raw_payloads` | Persistence | Source, endpoint, external ID/context, raw JSON, fetched timestamp, content hash | Raw facts must survive model changes |
| `transactions` | Persistence/Normalization | Transaction ID, league ID, type, status, created/updated timestamps, raw payload reference | Completed trades are primary; add/drop movement retained |
| `transaction_assets` | Persistence/Normalization | Transaction ID, roster/user, movement direction, asset key, player ID/pick fields, metadata | Supports add/drop and general movement facts |
| `trade_sides` | Persistence/Normalization | Transaction ID, side ID, roster/user, metadata | Multi-team trades must be representable |
| `trade_assets` | Persistence/Normalization | Transaction ID, side ID, asset key, player ID/pick fields, quantity/context | Draft-pick precision may be nullable |
| `ranking_runs` | Persistence/Valuation | Run ID, season, model version, config JSON, input summary, created timestamp | Reproducibility requires model/config metadata |
| `ranking_assets` | Persistence/Valuation | Run ID, rank, asset key, asset type, name, position/pick fields, value score, confidence fields | CSV and inspection rely on stable fields |
| `ranking_evidence` | Persistence/Valuation | Run ID, asset key, transaction/trade reference, contribution, recency, notes/outlier flag | Enables source-trade inspection |

### Schema Constraint Contract

The schema contract is inherited from `docs/loom/03-architecture.md`. Phase 5 tests must verify more than table existence.

| Contract Area | Required Test Evidence |
|---------------|------------------------|
| Required tables | Fresh migrated SQLite database includes users, leagues, league users, rosters, players, raw payloads, transactions, transaction assets, trade sides, trade assets, crawl runs, crawl frontier, fetched markers, league sync state, ranking runs, ranking assets, and ranking evidence |
| Primary keys | Every table has a primary key or composite primary key appropriate to its idempotency behavior |
| Idempotency constraints | Sleeper users, leagues, league users, rosters, transactions, crawl frontier items, fetched markers, league sync state, ranking assets, and ranking ranks cannot duplicate on repeated syncs |
| Foreign keys | Relationship tables reference their parent tables where SQLite can enforce the relationship |
| Raw JSON preservation | Raw/source payload JSON columns exist for users, leagues, rosters, transactions, transaction assets, trade assets, raw payloads, crawl runs, ranking runs, and ranking evidence |
| Draft-pick precision | Pick season, round, original roster, owner/current roster, and exact pick position fields exist where pick assets are stored; exact pick position is nullable |
| Ranking reproducibility | Ranking runs store model version, config JSON, input summary JSON, created timestamp, and ranking assets/evidence reference the run |

### Asset Identity Contract

Asset keys must be stable and shared by normalization, valuation, export, and inspection.

Initial convention:

```text
player:<sleeper_player_id>
pick:<season>:<round>:<original_owner_or_unknown>:<pick_number_or_unknown>
```

Rules:

- Player assets use Sleeper player IDs, not display names.
- Draft picks preserve known season, round, original owner, current owner context, and exact pick only when known.
- Unknown pick fields use the literal `unknown`, not empty strings.
- Asset keys are deterministic and never include league-specific display labels.
- CSV output may include human-readable labels, but labels do not replace asset keys.

---

## Test Strategy

### Testing Gap Status

The current test suite now covers the major phase gaps as executable contracts. Some checks still remain deferred because they need implementation tooling or a type-checking decision.

| Area | Status | Evidence |
|------|--------|----------|
| Repository method contracts for each repository | Covered by red contract tests | `tests/contracts/test_repository_contracts.py` |
| Alembic migration upgrade/downgrade checks | Covered by red contract tests | `tests/contracts/test_alembic_migrations_contract.py` |
| Rate limiter unit tests with fake clock | Covered by red unit tests | `tests/unit/test_rate_limiter.py` |
| Retry policy tests for retryable vs permanent failures | Covered by red unit tests | `tests/unit/test_retry_policy.py` |
| Endpoint contracts for leagues, league users, rosters, transactions, traded picks, and players | Covered by red contract tests | `tests/contracts/test_sleeper_client_contract.py` |
| More transaction fixtures: multi-team trades, exact pick positions, missing roster/user | Covered by red unit tests and fixtures | `tests/unit/test_transaction_normalizer_trades.py`, `tests/fixtures/sleeper/` |
| Valuation model fixture with exact expected ranking output | Covered by red unit tests | `tests/unit/test_valuation_model_v1.py`, `tests/fixtures/rankings/` |
| Confidence/outlier calculator unit tests | Covered by red unit tests | `tests/unit/test_confidence_and_outliers.py` |
| End-to-end fixture workflow test | Covered by red integration test | `tests/integration/test_full_fixture_workflow.py` |
| CLI option matrix tests | Partially covered by red CLI tests | `tests/cli/test_command_options.py`; add more options as commands are implemented |
| Live Sleeper smoke tests | Covered by opt-in skipped-by-default test | `tests/live/test_sleeper_live_smoke.py` |
| Type-checking policy | Deferred to CI bootstrap | Decide Pyright or mypy before making type checks required |
| CI/CD workflow file | Deferred to CI bootstrap | Add `.github/workflows/ci.yml` during `S1.9` after `uv.lock` exists |

### Coverage Matrix

| Area | Test Type | Owner | Required Before Merge |
|------|-----------|-------|-----------------------|
| Project scaffold | CLI smoke, import tests | Project Foundation | `trade-winds --help` works; package imports cleanly |
| Configuration | Unit and CLI error tests | Project Foundation | Env/default validation; missing seed username has clear error |
| App context | Unit/component tests | Service Boundary Design | Dependency wiring and test overrides are covered |
| Persistence schema | Migration/integration tests | Persistence | Fresh SQLite DB migrates; expected tables and constraints exist |
| Schema contract | Contract test using SQLAlchemy inspection | Persistence | Tables, keys, constraints, foreign keys, and JSON/raw columns match the architecture schema contract |
| Repositories | Integration tests | Persistence | Upserts are idempotent; queries return deterministic results |
| Sleeper client | Contract/unit tests with mocked HTTP | Sleeper Client | Endpoint methods parse fixtures, preserve raw JSON, handle errors |
| Rate limiting/retries | Unit tests with fake clock/client | Sleeper Client | Configured pacing and retry policy are deterministic |
| Discovery crawl | Component/integration tests with fake client | Crawl | Frontier resume, fetched markers, limits, and counts covered |
| Transaction sync | Component/integration tests with fixtures | Crawl/Normalization | Current-season transaction persistence and idempotency covered |
| Normalization | Unit/property tests | Normalization | Trades, add/drops, picks, missing fields, odd trades covered |
| Ranking model | Unit/component tests | Valuation | Scores, recency weighting, confidence, outlier flags covered |
| Ranking persistence | Integration tests | Valuation/Persistence | Runs/assets/evidence are written and queryable |
| Export | Unit/CLI tests | Export | Stable CSV columns, deterministic ordering, filters covered |
| Inspection | CLI/query tests | Inspection | Runs, rankings, asset evidence, and comparison views covered |
| End-to-end local workflow | Integration test | All | Fixture-backed discover/sync/rank/export/inspect path works |

### Required Test Fixtures

Fixture payloads should be small, named, and intentionally shaped around behavior:

| Fixture | Purpose |
|---------|---------|
| `user_seed.json` | Seed username resolves to a Sleeper user ID |
| `user_leagues_current_season.json` | User belongs to one or more current-season leagues |
| `league_users.json` | Discovery expands to league users |
| `league_rosters.json` | Roster context supports ownership and add/drop baseline logic |
| `transactions_completed_trade.json` | Simple two-team completed trade |
| `transactions_multiteam_trade.json` | Multi-side trade normalization |
| `transactions_add_drop.json` | Add/drop movement captured without becoming primary valuation signal |
| `transactions_weird_trade.json` | Odd trade preserved and flaggable |
| `traded_picks.json` | Draft-pick movement with nullable pick precision |
| `ranking_minimal_input.json` | Small deterministic ranking input for model tests |

Fixtures are source examples, not golden implementation outputs. Golden files may be added for CSV or CLI output only when the output format is intentionally stable.

---

## Acceptance Tests

| Requirement | Test | Evidence |
|-------------|------|----------|
| Configure a crawl | CLI/config tests for env-based seed username, DB path, request rate, limits, and missing config | Passing `tests/unit/test_settings.py` and `tests/cli/test_config_errors.py` |
| Run a resumable Sleeper crawl | Fake-client discovery test interrupts and resumes without duplicating users/leagues/frontier items | Passing `tests/integration/test_crawl_discovery_resume.py` |
| Store completed trade facts | Fixture transactions persist raw payloads plus normalized trade sides/assets | Passing `tests/integration/test_transaction_sync_persistence.py` |
| Store add/drop baseline facts | Fixture add/drop transactions persist movement and roster context without primary trade scoring | Passing `tests/unit/test_transaction_normalizer_add_drop.py` |
| Generate dynasty rankings | Ranking service reads only persisted facts and writes ranking run/assets/evidence | Passing `tests/integration/test_ranking_generation.py` |
| Explain ranking context | Ranking output includes sample counts, recency context, confidence fields, and source evidence | Passing `tests/unit/test_valuation_confidence.py` and inspection tests |
| Export rankings | CSV export writes stable columns and deterministic row order | Passing `tests/cli/test_export_rankings.py` |
| Inspect rankings | CLI/query tests cover runs, rankings filters, asset evidence, and latest-run behavior | Passing `tests/cli/test_inspect_commands.py` |
| Compare stability across runs | Two fixture ranking runs produce movement/unstable-asset comparison | Passing `tests/integration/test_ranking_comparison.py` |

---

## Integration Tests

| Integration Point | Test Scenario | Owner |
|-------------------|---------------|-------|
| CLI -> Settings -> AppContext | Command uses env/config and creates temp database context | Project Foundation |
| AppContext -> repositories | Services receive working repository bundle and session factory | Service Boundary Design/Persistence |
| Alembic -> SQLite | Fresh DB upgrades to head and expected constraints exist | Persistence |
| Sleeper client -> mocked HTTP | Endpoint methods call expected paths, parse payloads, and handle retryable failures | Sleeper Client |
| Crawl -> repositories -> fake Sleeper client | Discovery persists users/leagues/rosters/frontier and resumes | Crawl/Persistence |
| Transaction sync -> normalizer -> repositories | Fixture transactions produce raw and normalized facts idempotently | Crawl/Normalization/Persistence |
| Ranking -> persisted facts | Ranking generation performs no Sleeper calls and persists outputs | Valuation/Persistence |
| Export/Inspection -> query services | CLI and CSV read persisted ranking data without recalculating model outputs | Export/Inspection |
| Full fixture workflow | Temp DB runs fixture-backed discover, sync, rank, export, inspect | All |

---

## Check Automation Handoff

### Current Status

- **Runnable scaffold exists?** [ ] Yes [x] No
- **Dependency lockfile exists?** [ ] Yes [x] No
- **Tests currently expected to pass?** [ ] Yes [x] No
- **CI/check workflow exists?** [ ] Yes [x] No

CI/CD is **not set up yet**. This is intentional for the current moment because:

- The repository has contract tests that are expected to fail until implementation exists.
- `uv.lock` has not been generated yet.
- The package scaffold is not complete enough for a meaningful install/build check.
- Local pytest is not currently installed in the active environment.

CI/CD should become a dedicated bootstrap slice after S0/S1/S1.75 and before merge-gated implementation work. In the planning document this is `S1.9: CI Bootstrap`.

### Automation Bootstrap Plan

Add `.github/workflows/ci.yml` when the package scaffold can install with `uv` and the lockfile exists.

Initial workflow:

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: uv sync --locked
      - run: uv run ruff format --check .
      - run: uv run ruff check .
      - run: uv run pytest
```

Add these checks as the relevant implementation pieces land:

| Check | Add When | Blocking? |
|-------|----------|-----------|
| `uv sync --locked` | `uv.lock` exists | Yes |
| `uv run ruff format --check .` | Ruff config exists | Yes |
| `uv run ruff check .` | Ruff config exists | Yes |
| `uv run pytest` | First implementation slice is expected to pass the current contract suite | Yes |
| `uv run pytest --cov=trade_winds --cov-report=term-missing` | Package scaffold exists and first green suite is stable | Start informational, then blocking |
| Type checking | Pyright or mypy is selected | Start informational, then blocking |
| Alembic migration check | Alembic exists | Blocking for persistence changes |
| Live Sleeper smoke tests | Sleeper client has stable mocked tests | Non-blocking/manual only |

Live Sleeper tests must not run on normal pull requests. If they are added later, they should use a separate manual workflow or job guarded by repository secrets and `TRADE_WINDS_LIVE_SLEEPER=1`.

### Required Checks

- [ ] `uv sync --locked`
- [ ] `uv run ruff format --check .`
- [ ] `uv run ruff check .`
- [ ] `uv run pytest`
- [ ] `uv run pytest --cov=trade_winds --cov-report=term-missing`
- [ ] Type checking after the type checker is selected
- [ ] Alembic migration check after migrations exist

### Suggested Local Commands

Initial commands after scaffolding:

```bash
uv run pytest
uv run pytest tests/unit/test_transaction_normalizer_trades.py
uv run ruff check .
uv run ruff format --check .
```

Opt-in live API smoke tests:

```bash
TRADE_WINDS_LIVE_SLEEPER=1 uv run pytest tests/live
```

Live tests must be skipped by default unless `TRADE_WINDS_LIVE_SLEEPER=1` is set and required config is present.

### Deployment / Release Automation

MVP has no hosted deployment. CI gates local package quality and protects the TDD loop. Release artifacts are local CLI commands, SQLite databases under ignored local paths, and CSV outputs.

Promotion flow:

1. Feature branch or local slice has failing tests first.
2. Implementation passes focused tests.
3. Full CI checks pass.
4. Implementation notes are recorded in `docs/loom/06-implementation.md` when behavior materially changes architecture or planning assumptions.

Rollback for MVP means reverting the offending code change while preserving committed tests that describe the intended behavior, unless the contract itself is explicitly changed.

---

## Observability

### Metrics, Logs, and Alerts

| Signal | Purpose | Alert Threshold |
|--------|---------|-----------------|
| API request count by endpoint | Understand crawl cost and Sleeper usage | Local warning when configured max calls is near exhaustion |
| Retry count and failure count | Identify API instability or bad payload assumptions | Local warning on repeated endpoint failures |
| Crawl frontier pending/completed/failed counts | Confirm crawl progress and resumability | CLI summary shows non-zero failed items |
| Transaction normalization warnings | Surface payloads that need fixture coverage | Any new warning should create or update a test fixture |
| Ranking input counts | Explain model confidence and sparse data | CLI summary warns when eligible completed trades are below threshold |
| Outlier trade count | Preserve strange trades while making them visible | CLI summary shows outlier count |
| Export row count/path | Confirm inspection artifact creation | CLI error if zero rows unexpectedly exported |

No hosted alerts are required for MVP. Observability is local logs, CLI summaries, persisted run metadata, and inspectable database records.

---

## TDD Phase Gate

### Ready to Move to Implementation?

- [ ] Yes
- [x] No

### Template Gate Checks

- **Required tests/contracts identified?** [x] Yes
- **Automation/bootstrap handoff captured?** [x] Yes
- **Contract stability and rewrite approval policy captured?** [x] Yes
- **Known intentionally red tests documented?** [x] Yes

### Before Implementation Starts

- [ ] Create Python package scaffold and test directories.
- [ ] Add `pytest`, `pytest-cov`, `ruff`, `typer`, and selected HTTP mocking library to `pyproject.toml`.
- [ ] Add the first failing CLI/config tests for S0/S1.
- [ ] Add fixture directory structure.
- [ ] Add the schema contract test before database implementation.
- [ ] Generate `uv.lock` once `uv` is available.
- [ ] Add `.github/workflows/ci.yml` during S1.9 CI Bootstrap.
- [ ] Decide when CI becomes blocking for pull requests.
- [ ] Decide between `pytest-httpx` and `respx` during Sleeper client slice.
- [ ] Decide between Pyright and mypy during scaffold slice.

### Remaining Concerns

- We should keep the first tests focused on contracts and behavior, not internal implementation guesses.
- We should avoid overusing mocks for repositories; SQLite temp DB tests are cheap and give more confidence.
- We should treat real Sleeper responses as compatibility smoke tests, not the foundation of the suite.
- We should update this document when real payloads reveal new edge cases.

### Owner Decision

Proceed with a pytest-first TDD workflow. Implementation begins only after the first scaffold/config/CLI tests are written and intentionally failing.

---

## Reference Sources

- pytest documentation: https://docs.pytest.org/en/stable/contents.html
- Typer testing documentation: https://typer.tiangolo.com/tutorial/testing/
- Hypothesis documentation: https://hypothesis.readthedocs.io/
- Ruff formatter/linter documentation: https://docs.astral.sh/ruff/formatter/ and https://docs.astral.sh/ruff/linter/
- SQLAlchemy SQLite documentation: https://docs.sqlalchemy.org/21/dialects/sqlite.html
- Alembic autogenerate documentation: https://alembic.sqlalchemy.org/en/latest/autogenerate.html
