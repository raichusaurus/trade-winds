# Architecture

Design the Trade Winds MVP system architecture.

**Project Name:** trade-winds
**Date:** 2026-05-12
**Architecture Lead:** Codex + John Hightshue

---

## Overview

### Problem

Trade Winds needs a local-first system that can start from a configured Sleeper username, crawl the current-season Sleeper user-league graph, persist completed trade facts, and generate dynasty-oriented player and draft-pick rankings from those accepted trades.

The MVP is not a public product yet. It is a data and model validation loop with inspectable outputs: CSV export, concise CLI output, direct database/query inspection, and reusable service boundaries for a quick future web-app or admin API.

### Architectural Goals

- Keep the first implementation simple enough to build and debug quickly.
- Persist raw Sleeper facts faithfully so model iterations can be rerun without recrawling.
- Make crawling resumable through durable frontier, fetched markers, and run metadata.
- Isolate Sleeper integration, persistence, crawl orchestration, valuation logic, exports, and query services behind clear boundaries.
- Keep the CLI as an interface over reusable application services, so future web-app controls can call the same crawl, ranking, export, and query workflows without rewriting core logic.
- Prefer local-first and near-zero-cost infrastructure, while preserving a path to Postgres and scheduled execution later.
- Keep the first valuation model explainable and replaceable.
- Respect Sleeper API usage guidance with configurable throttling, retries, and progress visibility.

### Legacy Review Findings

The archived `trade-winds-legacy` repo should inform the new implementation, not constrain it.

| Legacy Area | Decision | Notes |
|-------------|----------|-------|
| Python crawler | Reuse idea | The queue-based user/league traversal is the right basic shape. Rebuild with persisted frontier and limits. |
| Sleeper integration modules | Reuse idea | Endpoint wrapping and response parsing are useful patterns. Expand coverage for transactions, rosters, picks, and players. |
| Pydantic models | Reuse idea | Keep typed parsing at the API boundary, but do not over-model every raw payload early. |
| Retry/backoff helper | Reuse idea | Keep retries with jitter, but make rate limits and user agent configurable. |
| In-memory storage | Discard | MVP requires SQLite, resumability, and queryable facts. |
| Planned FastAPI/Admin API | Defer with fast path | Public/admin API is out of scope for MVP controls, but application/query service boundaries should make admin endpoints quick to add. |
| Postgres/Docker-first roadmap | Defer | Preserve migration path, but do not add infra cost or operational weight for MVP. |

---

## System Architecture

### High-Level Design

```text
             local config / .env
                    |
                    v
+-------------------+-------------------+
|                  CLI                  |
| crawl | rank | export | inspect       |
+---------+-----------+-----------------+
          |
          v
+---------+---------------------------+
| Application Services                |
| crawl, rank, export, ranking query  |
+---------+-----------+---------------+
          |           |          |
          v           v          v
+---------+--+   +----+-----+  +-------------------+
| Crawl      |   | Valuation|  | CSV + CLI Inspect |
| Orchestrator|  | Engine   |  +-------------------+
+-----+------+   +----+-----+
      |               |
      v               |
+-----+------+        |
| Sleeper    |        |
| Client     |        |
+-----+------+        |
      |               |
      v               |
 Sleeper API          |
                      |
          v           v
+-------------------------------+
| Persistence Layer             |
| repositories, upserts, queries|
+---------------+---------------+
                |
                v
+-------------------------------+
| SQLite Database               |
| normalized facts, crawl state,|
| rankings, source evidence     |
+-------------------------------+
```

### Major Components

| Component | Purpose | Responsibility |
|-----------|---------|----------------|
| Configuration | Load local operator settings | Seed username, season, database path, default request rate, runtime rate controls, limits, output paths, future lookback settings |
| CLI | Primary MVP operator interface | Parse commands and options, load config, call application services, print operator feedback |
| Application Services | Interface-independent workflow boundary | Run crawl, resume crawl, generate rankings, export CSV, query rankings and evidence for CLI/web/API surfaces |
| Sleeper Client | External API boundary | Typed endpoint methods, adaptive throttling, retries, response validation, raw payload capture |
| Crawl Orchestrator | Graph traversal and collection | Run full discovery crawls and incremental transaction syncs, fetch current-season league data and transactions, update frontier and run metadata |
| Persistence Layer | Durable storage boundary | SQLite schema access, upserts, fetched markers, raw facts, ranking outputs |
| Transaction Normalizer | Convert Sleeper transactions into model-ready facts | Normalize trades, add/drop assets, waiver/free-agent movement, draft picks, and source payloads |
| Valuation Engine | Generate ranking outputs | Time-weighted trade constraints, add/drop baseline calibration, asset scores, confidence metrics, outlier flags, source evidence |
| Exporter | File-based inspection output | Stable CSV rankings and optional comparison files |
| Inspection Adapter | Optional thin local surface | CLI inspection commands first; optional minimal FastAPI read-only/admin adapter only if it accelerates the web/API transition |

### Component Interactions

- The CLI loads configuration, creates an application context, and calls application services.
- Application services own workflow-level orchestration and are designed to be reused by a future web app or scheduled worker.
- Crawl services call the crawl orchestrator, which pulls pending frontier work from SQLite and calls the Sleeper client.
- The Sleeper client owns HTTP behavior: base URL, user agent, adaptive request pacing, retry/backoff, and response parsing.
- The crawl orchestrator stores raw payload snapshots and normalized rows in the same transaction where practical.
- Ranking services read persisted transaction facts, with completed trades as the primary valuation signal and add/drop movement used mainly to calibrate each league's rosterable-player line and the bottom of the scale; they do not call Sleeper directly.
- The valuation engine writes ranking runs, ranking rows, confidence metrics, outlier flags, and source-trade contributions.
- CSV export and inspection commands read persisted ranking outputs through query services.

### Service Interaction Diagrams

The high-level architecture should be implemented as a set of small services with clear call directions. Names can be refined during implementation, but the dependency shape should remain stable: interfaces call application services, application services coordinate domain services and repositories, and domain services do not import CLI or future web modules.

#### Runtime Composition

```text
CLI command
  |
  v
AppContext
  |-- Settings
  |-- Database session factory
  |-- SleeperClient
  |-- Repository bundle
  |
  v
Application service
```

`AppContext` is the composition point. It wires configuration, database sessions, HTTP clients, and repositories together so commands stay thin and future FastAPI routes can reuse the same services.

#### Crawl Discovery Flow

```text
Crawl CLI
  |
  v
CrawlApplicationService.discover()
  |
  v
CrawlOrchestrator.run_discovery()
  |        |
  |        +--> CrawlStateRepository
  |        |      - create/update crawl_runs
  |        |      - lease/update crawl_frontier items
  |        |      - write fetched_markers
  |        |
  |        +--> SleeperClient
  |        |      - get_user_by_username()
  |        |      - get_user_leagues()
  |        |      - get_league_users()
  |        |      - get_league_rosters()
  |        |
  |        +--> SleeperFactRepository
  |               - upsert users
  |               - upsert leagues
  |               - upsert league_users
  |               - upsert rosters
  |
  v
CrawlSummary
```

Discovery owns graph expansion. It should persist progress as it goes, so interruption loses as little work as practical and the next run can resume from durable frontier state.

#### Transaction Sync Flow

```text
Crawl CLI
  |
  v
CrawlApplicationService.sync_transactions()
  |
  v
TransactionSyncService.run()
  |        |
  |        +--> LeagueSyncRepository
  |        |      - read known leagues
  |        |      - read/update league_sync_state
  |        |
  |        +--> SleeperClient
  |        |      - get_league_transactions()
  |        |      - get_traded_picks()
  |        |
  |        +--> TransactionNormalizer
  |        |      - normalize transaction
  |        |      - normalize trade sides/assets
  |        |      - normalize add/drop movement
  |        |
  |        +--> TransactionRepository
  |               - upsert raw transactions
  |               - upsert transaction_assets
  |               - upsert trade_sides
  |               - upsert trade_assets
  |
  v
TransactionSyncSummary
```

Transaction sync should store facts, not valuation opinions. Completed trades, add/drop movement, picks, and raw payloads are preserved so future model versions can reinterpret the same source material.

#### Ranking Flow

```text
Rank CLI
  |
  v
RankingApplicationService.generate()
  |
  v
ValuationEngine.score()
  |        |
  |        +--> RankingInputRepository
  |        |      - load completed trade sides/assets
  |        |      - load add/drop baseline facts
  |        |      - load league/player/pick context
  |        |
  |        +--> ValuationModel
  |        |      - calculate asset scores
  |        |      - calculate confidence metrics
  |        |      - identify outlier signals
  |        |
  |        +--> RankingOutputRepository
  |               - create ranking_runs
  |               - write ranking_assets
  |               - write ranking_evidence
  |
  v
RankingSummary
```

`ValuationModel` is the replaceable algorithm boundary. It receives normalized facts and configuration, then returns scores, confidence fields, and evidence. Different model versions should be able to read the same persisted facts and write separate ranking runs.

#### Export and Inspection Flow

```text
Export / Inspect CLI
  |
  v
InspectionApplicationService
  |        |
  |        +--> RankingQueryService
  |        |      - list ranking runs
  |        |      - list/filter ranking assets
  |        |      - fetch asset evidence
  |        |      - compare ranking runs
  |        |
  |        +--> CsvExporter
  |               - write stable ranking CSV
  |
  v
Terminal table / CSV file
```

Inspection services should be read-oriented. They can format terminal output and CSV files, but they should not own crawl, normalization, or scoring behavior.

### Initial Service and Class Map

This is a starting map for implementation, not a promise that every class name must survive unchanged. If code reveals better names, update this architecture note and the planning ownership map together.

| Module Area | Primary Classes / Services | Role |
|-------------|----------------------------|------|
| `config` | `Settings`, `CrawlLimits`, `RateLimitSettings`, `OutputSettings` | Load operator config, default limits, paths, and request behavior |
| `app` | `AppContext`, `ServiceFactory` | Compose settings, database sessions, clients, repositories, and application services |
| `cli` | Typer command modules | Parse options, call application services, render concise output |
| `sleeper` | `SleeperClient`, `RateLimiter`, `RetryPolicy`, boundary Pydantic models | Fetch Sleeper API data with polite request behavior and typed boundaries |
| `db` | SQLAlchemy models, `SessionFactory`, Alembic migrations | Define database schema and migration path |
| `repositories` | `CrawlStateRepository`, `SleeperFactRepository`, `TransactionRepository`, `RankingInputRepository`, `RankingOutputRepository`, `RankingQueryRepository` | Isolate SQL/database access from domain services |
| `crawl` | `CrawlApplicationService`, `CrawlOrchestrator`, `TransactionSyncService`, `FrontierService` | Coordinate discovery and transaction sync workflows |
| `transactions` | `TransactionNormalizer`, `TradeSideBuilder`, `AssetKeyFactory` | Convert raw Sleeper transactions into normalized facts and stable asset identities |
| `valuation` | `RankingApplicationService`, `ValuationEngine`, `ValuationModel`, `ConfidenceCalculator`, `OutlierDetector` | Generate versioned ranking runs from persisted facts |
| `inspection` | `InspectionApplicationService`, `RankingQueryService`, `RunComparisonService` | Read ranking outputs, evidence, and run metadata for CLI/query inspection |
| `exports` | `CsvExporter` | Write stable CSV outputs from persisted ranking data |

### Component Internal Contracts

The next phase should turn these into explicit contracts and tests. This section is intentionally more detailed than the box diagram: it describes what each component owns, what it receives, what it returns, and what behavior should be protected by tests.

#### Configuration and App Context

| Item | Detail |
|------|--------|
| Owns | Operator settings, environment/default resolution, local paths, service composition |
| Key classes | `Settings`, `CrawlLimits`, `RateLimitSettings`, `OutputSettings`, `AppContext`, `ServiceFactory` |
| Inputs | Environment variables, optional ignored local config, CLI option overrides |
| Outputs | Validated settings, database session factory, configured `SleeperClient`, repository bundle, application services |
| Must not do | Fetch Sleeper data, write domain rows, run ranking logic |
| Contract tests | Missing seed username produces clear error; default paths resolve into ignored local directories; CLI overrides take precedence over defaults; `AppContext` can construct services without side effects beyond opening configured resources |

Expected configuration keys include:

```text
TRADE_WINDS_SEED_USERNAME
TRADE_WINDS_SEASON
TRADE_WINDS_DB_PATH
TRADE_WINDS_OUTPUT_DIR
TRADE_WINDS_REQUESTS_PER_SECOND
TRADE_WINDS_MAX_USERS
TRADE_WINDS_MAX_LEAGUES
TRADE_WINDS_MAX_API_CALLS
TRADE_WINDS_MAX_RUNTIME_SECONDS
```

#### CLI

| Item | Detail |
|------|--------|
| Owns | Command names, option parsing, terminal rendering, process exit codes |
| Key modules | `cli.main`, `cli.crawl`, `cli.rank`, `cli.export`, `cli.inspect` |
| Inputs | User command/options and environment |
| Outputs | Human-readable summaries, CSV files through exporter service, non-zero exit codes for command failures |
| Must not do | Import SQLAlchemy models directly for business behavior, call Sleeper directly, contain ranking math |
| Contract tests | `trade-winds --help` renders; missing config exits clearly; each command calls the expected application service; output includes run IDs/counts where relevant |

Initial command shape:

```text
trade-winds crawl discover
trade-winds crawl transactions
trade-winds rank
trade-winds export rankings
trade-winds inspect runs
trade-winds inspect rankings
trade-winds inspect asset <asset_key>
trade-winds inspect compare
```

#### Sleeper Client

| Item | Detail |
|------|--------|
| Owns | Sleeper HTTP transport, endpoint paths, request pacing, retries/backoff, response parsing at API boundary |
| Key classes | `SleeperClient`, `RateLimiter`, `RetryPolicy`, endpoint response models |
| Inputs | Endpoint parameters such as username, user ID, league ID, season, transaction round/page where applicable |
| Outputs | API result objects that include parsed fields plus original raw JSON payloads |
| Must not do | Write to SQLite, decide crawl frontier, normalize transactions into project tables, assign values |
| Contract tests | Endpoint URL construction; retry/backoff on transient failures; rate limiter is invoked; malformed/partial payloads preserve raw JSON; 404/user-not-found maps to a controlled error |

Initial endpoint methods:

```text
get_user_by_username(username)
get_user_leagues(user_id, season)
get_league_users(league_id)
get_league_rosters(league_id)
get_league_transactions(league_id, season)
get_traded_picks(league_id)
get_players()
```

#### Persistence and Repositories

| Item | Detail |
|------|--------|
| Owns | SQLite schema, migrations, SQLAlchemy sessions, database-specific query/upsert behavior |
| Key classes | SQLAlchemy models, `SessionFactory`, repository classes |
| Inputs | Normalized facts, raw payload JSON, run metadata, ranking outputs |
| Outputs | Persisted rows, query DTOs/read models, idempotent upsert results |
| Must not do | Make HTTP requests, parse CLI options, contain valuation algorithms |
| Contract tests | Fresh migration creates all tables; primary keys prevent duplicate facts; upserts update `last_seen_at`/state without duplicating; query methods return deterministic read models |

Repository split:

| Repository | Owns |
|------------|------|
| `CrawlStateRepository` | `crawl_runs`, `crawl_frontier`, `fetched_markers` |
| `SleeperFactRepository` | `users`, `leagues`, `league_users`, `rosters`, `players` |
| `LeagueSyncRepository` | known league selection and `league_sync_state` |
| `TransactionRepository` | `transactions`, `transaction_assets`, `trade_sides`, `trade_assets` |
| `RankingInputRepository` | read-only model inputs from persisted facts |
| `RankingOutputRepository` | `ranking_runs`, `ranking_assets`, `ranking_evidence` writes |
| `RankingQueryRepository` | inspection/read queries over ranking outputs and evidence |

#### Crawl Application and Orchestration

| Item | Detail |
|------|--------|
| Owns | Workflow-level discovery and transaction sync coordination |
| Key classes | `CrawlApplicationService`, `CrawlOrchestrator`, `TransactionSyncService`, `FrontierService` |
| Inputs | Settings, crawl limits, seed username, repositories, `SleeperClient`, active season |
| Outputs | `CrawlSummary`, `TransactionSyncSummary`, persisted crawl state/facts |
| Must not do | Calculate rankings, format CSVs, expose web routes |
| Contract tests | Discovery seeds frontier from username; limits stop expansion; already-fetched markers prevent redundant fetches; interrupted/in-progress frontier items can be retried; run counts/errors are recorded |

Discovery service responsibilities:

```text
1. Start crawl_run.
2. Resolve seed username to Sleeper user.
3. Enqueue seed user and discovered leagues/users.
4. Lease pending frontier items.
5. Fetch league users and rosters.
6. Upsert facts and fetched markers.
7. Stop on configured limits.
8. Finish run with counts/errors.
```

Transaction sync responsibilities:

```text
1. Start transaction_sync crawl_run.
2. Select known leagues for active season.
3. Read league_sync_state.
4. Fetch current-season transactions and traded picks.
5. Normalize transaction facts.
6. Upsert transaction rows/assets/trade projections.
7. Update league high-watermark state.
8. Finish run with counts/errors.
```

#### Transaction Normalization

| Item | Detail |
|------|--------|
| Owns | Conversion from raw Sleeper transaction payloads to normalized, model-ready facts |
| Key classes | `TransactionNormalizer`, `TradeSideBuilder`, `AssetKeyFactory` |
| Inputs | Raw transaction payload, league ID/season, league roster/user context, traded-pick payloads where needed |
| Outputs | Transaction fact DTO, generic transaction asset DTOs, trade side DTOs, trade asset DTOs, stable asset keys |
| Must not do | Fetch API data, write directly to SQLite, infer value/rank |
| Contract tests | Completed trade with players creates correct sides/assets; trade with picks preserves season/round/original owner/current owner and nullable exact position; add/drop creates added/dropped movement; strange but complete trades are preserved rather than discarded |

Asset key convention should be stable before valuation/export work starts:

```text
player:<sleeper_player_id>
pick:<season>:<round>:<original_roster_id>
pick:<season>:<round>:<original_roster_id>:<pick_position>  # only when exact pick is known
```

The normalizer stores movement facts without interpreting them:

```text
added
dropped
traded_away
traded_for
draft_pick
```

#### Valuation and Ranking

| Item | Detail |
|------|--------|
| Owns | Interpretation of persisted market facts into ranking outputs |
| Key classes | `RankingApplicationService`, `ValuationEngine`, `ValuationModel`, `ConfidenceCalculator`, `OutlierDetector` |
| Inputs | Completed trade sides/assets, add/drop baseline facts, player metadata, league context, ranking config |
| Outputs | Versioned ranking run, ranked assets, value scores, confidence metrics, outlier indicators, source evidence |
| Must not do | Call Sleeper, mutate raw transaction facts, require external ranking priors in MVP |
| Contract tests | Ranking reads persisted facts only; two model versions can write separate ranking runs; scores are deterministic for the same input/config; evidence rows trace ranked assets back to source trades |

Replaceable model boundary:

```text
ValuationModel.score(input: RankingInput, config: RankingConfig) -> RankingResult
```

Where:

```text
RankingInput
  completed_trades
  trade_sides
  trade_assets
  add_drop_facts
  league_context
  player_metadata

RankingResult
  model_version
  config
  assets[]
  evidence[]
  summary_counts
```

#### Export and Inspection

| Item | Detail |
|------|--------|
| Owns | Human inspection of persisted ranking outputs |
| Key classes | `InspectionApplicationService`, `RankingQueryService`, `RunComparisonService`, `CsvExporter` |
| Inputs | Ranking run ID or `latest`, asset key filters, asset type/position filters, output path |
| Outputs | Terminal tables/summaries, CSV files, run comparison rows |
| Must not do | Generate new rankings implicitly, call Sleeper, mutate source facts |
| Contract tests | CSV has stable columns; ranking filters are deterministic; asset inspection returns evidence; compare highlights movement between two runs |

Initial CSV columns:

```text
ranking_run_id
model_version
rank
asset_key
asset_kind
display_name
position
value_score
confidence_label
sample_count
league_count
recency_weight_sum
direct_signal_count
outlier_signal_count
```

### Dependency Rules

- CLI modules may import application services; application services must not import CLI modules.
- Future FastAPI modules may import the same application/query services; domain services must not import FastAPI modules.
- Sleeper client modules must not write to the database directly.
- Repositories may know SQLAlchemy details; domain services should depend on repository methods rather than direct SQL queries where practical.
- Transaction normalization may read raw Sleeper payloads and league context, but it should not assign player values.
- Valuation models may read normalized facts and write ranking outputs, but they should not call Sleeper.
- Export and inspection services should read persisted outputs and evidence; they should not trigger crawls or ranking generation implicitly.

### Initial CLI Commands

Planning should treat the CLI as the MVP control surface. Exact option names can be refined during implementation, but the initial command contract should include:

| Command | Purpose | Primary Service |
|---------|---------|-----------------|
| `trade-winds crawl discover` | Run or resume graph discovery for users, leagues, league users, and rosters | Crawl application service |
| `trade-winds crawl transactions` | Run initial or incremental transaction sync for known leagues | Crawl application service |
| `trade-winds rank` | Generate a ranking run from persisted transaction facts | Ranking application service |
| `trade-winds export` | Write ranking outputs such as CSV files | Export application service |
| `trade-winds inspect` | Inspect ranking rows, source evidence, run metadata, and baseline context from persisted data | Ranking/query services |

The commands should be thin wrappers over application services so a future scheduler, FastAPI admin route, or web app can reuse the same workflows.

### Web-App / Admin API Transition Boundary

CLI first is an interface choice, not an internal architecture choice. The CLI should stay thin: it should parse arguments, call application services, and render terminal output. Core workflows should not import CLI modules or depend on terminal-specific behavior.

A future web app or admin API should be able to reuse the same service layer:

| Future Web/API Need | Reusable MVP Boundary |
|---------------------|-----------------------|
| Start or resume a crawl | Crawl application service |
| Show crawl progress | Crawl run and frontier query services |
| Generate rankings | Ranking application service |
| Download CSV | Export application service |
| Show rankings table | Ranking query service |
| Show source trades for an asset | Ranking evidence query service |

This keeps the later transition closer to adding FastAPI routes and UI screens than rewriting the crawler, persistence layer, or valuation engine.

---

## Technology Stack

### Decisions by Layer

#### Language and Runtime

- **Technology:** Python 3.12+
- **Justification:** Matches the legacy proof of concept, is excellent for data crawling/modeling, and keeps CLI, crawler, ranking, inspection, and future API backend code in one language.
- **Alternatives Considered:** TypeScript/Node, Go.
- **Tradeoffs:** Python is less ideal for a highly interactive frontend, but the MVP is data-heavy and local-first.

#### CLI

- **Technology:** Typer
- **Justification:** Clean command structure, typed options, friendly help output, and straightforward testing.
- **Alternatives Considered:** Click, argparse.
- **Tradeoffs:** Adds a small dependency over standard library `argparse`.
- **Boundary Rule:** CLI modules should depend on application services; application services should not depend on CLI modules.

#### HTTP and Validation

- **Technology:** `httpx` plus Pydantic
- **Justification:** `httpx` supports modern sync/async HTTP patterns if crawling later becomes concurrent; Pydantic keeps the API boundary explicit.
- **Alternatives Considered:** `requests`, raw dictionaries only.
- **Tradeoffs:** More structure up front, but fewer ambiguous payload assumptions later.

#### Persistence

- **Technology:** SQLite with SQLAlchemy 2.x and Alembic
- **Justification:** SQLite satisfies local-first persistence and queryability; SQLAlchemy keeps a path to Postgres; Alembic makes schema evolution explicit.
- **Alternatives Considered:** Raw `sqlite3`, SQLModel, DuckDB, Postgres from day one.
- **Tradeoffs:** SQLAlchemy adds ceremony, but the schema will be central to crawl resumability and model iteration.

#### Valuation

- **Technology:** Python service module using persisted trade facts; likely `numpy`/`scipy` only if the baseline model needs numerical solving.
- **Justification:** Start with explainable, testable model code before introducing specialized ranking infrastructure.
- **Alternatives Considered:** ML libraries, graph databases, external notebooks.
- **Tradeoffs:** A simple model may be noisy, but it is easier to inspect and replace.

#### Inspection and Future API

- **Technology:** CLI inspection commands and CSV for MVP; optional minimal FastAPI adapter if needed.
- **Justification:** A throwaway local dashboard would likely be replaced quickly by the real web app. MVP should invest in reusable query/application services instead of disposable UI.
- **Alternatives Considered:** FastAPI/Jinja dashboard, Streamlit, React/Vite, static CSV viewer.
- **Tradeoffs:** Less visual in the first MVP, but faster to validate the data/model and cleaner for a near-term web-app/admin API transition.
- **Boundary Rule:** Any FastAPI routes added during MVP should call query/application services directly; they should not own crawl, ranking, export, or inspection business logic.

#### Infrastructure

- **Hosting:** Local machine for MVP.
- **Containerization:** Deferred; add Docker only if it helps repeatability or cloud fallback.
- **Message Queue:** None for MVP. SQLite-backed frontier is the job queue.
- **Caching:** Persist raw API payload snapshots and fetched markers in SQLite; no Redis.

---

## Data Design

### Core Data Model

```text
users
  sleeper_user_id (PK)
  display_name
  raw_payload_json
  first_seen_at
  last_seen_at

leagues
  sleeper_league_id (PK)
  season
  name
  total_rosters
  roster_positions_json
  bench_slots
  taxi_slots
  ir_slots
  settings_json
  scoring_settings_json
  raw_payload_json
  first_seen_at
  last_seen_at

league_users
  sleeper_league_id (FK)
  sleeper_user_id (FK)
  roster_id
  display_name_at_fetch
  metadata_json

rosters
  sleeper_league_id (FK)
  roster_id
  sleeper_user_id (nullable FK)
  player_count
  starters_json
  players_json
  roster_value_context_json
  raw_payload_json

players
  sleeper_player_id (PK)
  full_name
  position
  team
  metadata_json
  fetched_at

transactions
  sleeper_transaction_id
  sleeper_league_id (FK)
  season
  type
  status
  created_at
  status_updated_at
  raw_payload_json
  PRIMARY KEY (sleeper_league_id, sleeper_transaction_id)

transaction_assets
  id (PK)
  transaction_id
  league_id
  roster_id
  sleeper_user_id (nullable FK)
  movement_kind ('added' | 'dropped' | 'traded_away' | 'traded_for' | 'draft_pick')
  asset_kind ('player' | 'pick')
  sleeper_player_id (nullable FK)
  pick_season
  pick_round
  pick_original_roster_id
  pick_owner_roster_id
  pick_position
  raw_asset_json

trade_sides
  id (PK)
  transaction_id
  league_id
  roster_id
  sleeper_user_id (nullable FK)

trade_assets
  id (PK)
  trade_side_id (FK)
  asset_kind ('player' | 'pick')
  sleeper_player_id (nullable FK)
  pick_season
  pick_round
  pick_original_roster_id
  pick_owner_roster_id
  pick_position
  raw_asset_json

crawl_runs
  id (PK)
  run_type ('discovery' | 'transaction_sync' | 'metadata_refresh')
  started_at
  finished_at
  status
  seed_username_hash_or_label
  season
  transaction_sync_since
  limits_json
  counts_json
  errors_json

crawl_frontier
  id (PK)
  entity_type ('user' | 'league')
  entity_id
  status ('pending' | 'in_progress' | 'done' | 'failed')
  priority
  attempts
  last_error
  updated_at

fetched_markers
  entity_type
  entity_id
  season
  fetch_kind
  fetched_at
  high_watermark
  source_run_id

league_sync_state
  sleeper_league_id (PK, FK)
  season
  first_transaction_fetch_at
  last_transaction_fetch_at
  last_seen_transaction_timestamp
  last_seen_transaction_id
  transaction_backfill_complete
  updated_at

ranking_runs
  id (PK)
  created_at
  season
  model_version
  config_json
  trade_count
  asset_count

ranking_assets
  ranking_run_id (FK)
  asset_key
  rank
  asset_kind
  display_name
  position
  value_score
  confidence_label
  sample_count
  league_count
  recency_weight_sum
  direct_signal_count
  outlier_signal_count

ranking_evidence
  ranking_run_id (FK)
  asset_key
  transaction_id
  league_id
  contribution_weight
  evidence_json
```

### Entity Notes

- Trade Winds should prefer normalized relational tables for operational queries, ranking, inspection reads, and future API reads.
- Raw Sleeper payloads should be retained as audit/debug snapshots for facts that may need re-normalization later, not used as the primary query shape.
- Player identity is Sleeper player ID. Display fields come from locally stored player metadata snapshots.
- Draft picks are first-class assets. Exact pick position remains nullable unless Sleeper data supports it.
- `transaction_assets` is the normalized fact table for all transaction asset movement. `trade_sides` and `trade_assets` are trade-specific projections used by the valuation model's primary trade-balance signal.
- League settings, roster settings, positional starter slots, bench depth, taxi slots, IR slots, and scoring settings are stored early because add/drop baseline calibration depends on league context, even if MVP rankings start as one global dynasty baseline.
- Ranking outputs are stored as run outputs so stability comparisons can use the same database.

### Crawl Modes and State

Trade Winds has two main crawl rhythms:

| Mode | Purpose | Expected Use | Primary State |
|------|---------|--------------|---------------|
| Discovery crawl | Expand the known Sleeper user/league graph | Manual MVP command; later schedulable with configurable limits | `crawl_frontier`, `fetched_markers`, users, leagues, league users, rosters |
| Transaction sync | Fetch new transactions from known leagues | Manual MVP command after initial backfill; later schedulable incremental sync | `league_sync_state`, `fetched_markers`, transactions, trade sides, trade assets |
| Metadata refresh | Refresh player metadata and stale league/settings data | Occasional maintenance | `fetched_markers`, players, leagues |

The initial transaction sync for a league should backfill the available current-season transaction data. Later transaction syncs should use league-level high-watermark state to request or filter only transactions newer than the last successful sync where the Sleeper API allows it. If the API endpoint returns broader transaction pages, Trade Winds should still deduplicate by stable transaction keys and stop processing once already-seen transactions are reached.

### Runtime Rate Control

Request rate should be configurable before a run and adjustable while a crawl is running. The crawler should start from a conservative default, then allow an operator or future admin API to change the effective requests-per-second for the active run without restarting it.

Runtime rate control should support:

- A configured default request rate.
- A minimum and maximum allowed request rate.
- A persisted or in-memory active run override.
- Automatic slowdown after rate-limit responses, repeated transient failures, or other API stress signals.
- Manual adjustment through CLI first, with the same control exposed through a future admin API.
- Progress output that shows the current effective rate and any automatic backoff state.

The rate limiter should live inside the Sleeper client or a shared HTTP utility, not inside CLI command code, so every caller uses the same pacing behavior.

### Crawl State Datapoints

| State | Why It Exists | Example Use |
|-------|---------------|-------------|
| `crawl_runs.run_type` | Separates graph discovery from transaction sync and metadata refresh | Compare a full discovery run against an incremental transaction sync |
| `crawl_runs.status` | Records whether a run completed, failed, or was interrupted | Resume safely and report failed runs in CLI, inspection output, or future admin UI |
| `crawl_runs.limits_json` | Captures run-specific bounds | Know whether a crawl stopped because of max leagues, max users, max calls, or runtime |
| `crawl_runs.counts_json` | Captures operational totals | Show fetched users, fetched leagues, new leagues, transactions processed, trades stored |
| `crawl_runs.errors_json` | Keeps run-level error summaries | Debug API failures without losing the whole run history |
| `crawl_frontier` | Durable graph-discovery queue | Resume user/league expansion after interruption |
| `crawl_frontier.status` | Tracks pending, in-progress, done, and failed graph nodes | Retry failed users/leagues without restarting from the seed |
| `fetched_markers` | Records fetch completion by entity and fetch kind | Avoid refetching league users, rosters, or transactions unnecessarily |
| `fetched_markers.high_watermark` | Stores generic progress markers for fetch kinds that support incremental progress | Track a last page, timestamp, or cursor-like value when available |
| `league_sync_state` | Stores transaction-sync progress for each known league | After initial backfill, fetch/process only transactions since the last seen transaction |

### Data Flow

1. Operator runs `trade-winds crawl discover`, `trade-winds crawl transactions`, or a combined `trade-winds crawl` command.
2. Configuration resolves seed username, season, rate limit, crawl limits, and database path.
3. Crawler records a typed `crawl_runs` row.
4. Discovery crawls seed or resume `crawl_frontier`, then fetch users, leagues, league users, and rosters.
5. Transaction syncs iterate known leagues, use `league_sync_state` for initial backfill versus incremental fetch behavior, and fetch transaction/traded-pick data.
6. Sleeper client fetches user, league, roster, transaction, traded-pick, and player metadata endpoints as requested by the active crawl mode.
7. Persistence layer upserts normalized users, leagues, rosters, transactions, transaction assets, trade sides, trade assets, raw audit payloads, and fetched markers.
8. Transaction normalizer stores completed trade sides/assets and add/drop movement for players and draft picks where present.
9. Operator runs `trade-winds rank`.
10. Valuation engine reads completed trades plus supporting transaction movement, applies recency weighting, scores assets, derives confidence context and outlier flags, then writes a `ranking_runs` output.
11. Operator inspects results through CLI summary, CSV export, direct database/query inspection, or an optional minimal FastAPI adapter.

### Storage Strategy

- **Application data:** SQLite database in a configurable local path, defaulting to an ignored local data directory.
- **Raw API data:** JSON columns in SQLite for audit/debug snapshots; normalized columns and tables are the primary application data shape.
- **Ranking exports:** CSV files in a configurable ignored output directory; database remains the source for reproducible outputs.
- **Logs:** Structured console logs for MVP. Optional file logs can be added if crawl runs become long.
- **Backups:** Manual copy of the SQLite file for MVP. Automated backups only become relevant if cloud fallback is used.

---

## Integration Points

### External APIs / Services

| Service | Purpose | Integration |
|---------|---------|-------------|
| Sleeper API | Source for users, leagues, rosters, transactions, traded picks, and players | Read-only HTTP client with configurable user agent, request rate, retries, and raw payload persistence |

### Sleeper Endpoint Families

- User by username.
- User leagues for NFL season.
- League users.
- League rosters.
- League transactions for current season.
- Traded draft picks where needed to enrich pick assets.
- Players metadata snapshot.

### Database Integrations

| System | Type | Purpose |
|--------|------|---------|
| SQLite | Local relational database | MVP persistence, crawl state, raw facts, ranking outputs |
| Postgres | Future relational database | Optional migration path if cloud execution or larger datasets justify it |

### Events and Queues

No external queue is used for MVP. `crawl_frontier` is the durable queue. Status transitions should be explicit enough that an interrupted `in_progress` item can be retried safely on the next run.

---

## Valuation Architecture

### Baseline Model Shape

The first model should keep completed trades as the primary valuation signal. Each completed trade becomes a weighted constraint between assets. A trade side is treated as a bundle of player and pick assets. The model estimates relative asset scores so the total value on both sides of accepted trades is as balanced as possible, with more recent trades carrying more weight.

Add/drop transactions should be framed mainly as baseline calibration signals, not as equal evidence to completed trades. More specifically, they help estimate each league's rosterable-player line: the rough point where a player moves from worth holding on a roster to freely replaceable in that league context. A dropped player implies one or more weaker claims:

- The player was near or below that league's rosterable-player line at that time.
- The player was below that specific team's roster threshold at that time.
- The player may have had little or no trade market in that league context.
- The player was less valuable to that manager than the player added, if the transaction includes a corresponding add.
- The signal is context-sensitive because drops can be driven by league size, roster size, bench depth, positional starter limits, taxi/IR rules, injuries, bye weeks, league format, or temporary need.

Model v1 should persist and expose add/drop signals, but use them conservatively to anchor the lower end of the scale. Repeated drops can suggest that an asset is near the rosterable-player line or near zero in comparable roster contexts. A drop in a shallow 10-team league should not carry the same baseline implication as a drop in a deep 14-team dynasty league. A drop from a monster roster should also be treated as weaker evidence that the player is unrosterable generally, because strong teams may cut players that weaker teams would still hold. Drops should not operate like normal pairwise trade constraints, and they should not materially move mid-tier or high-value players with meaningful accepted-trade samples.

Trade Winds should stay trade-derived for primary rankings: no external ranking priors or manual market anchors in MVP. Add/drop signals are still internal observed behavior from Sleeper transactions, so they can be used to locate the baseline/zero region without changing that principle.

Add/drop baseline calibration should consider:

- League size, using total rosters.
- Roster size and bench depth.
- Positional starter requirements and limits, including superflex/flex behavior.
- Taxi squad and IR slots where available.
- Player position and scarcity in the relevant roster format.
- The dropping team's roster strength, depth, contention context if inferable, and positional depth.
- Whether the dropped player would likely be above or below the rosterable-player line for an average team in that league.
- Whether the transaction was an add/drop pair, waiver claim, free-agent add, or pure drop.

### Required Model Boundaries

- Input: persisted completed trades, trade assets, add/drop movement for baseline calibration, timestamps, league size, roster size, positional limits, team roster context, league context, and configuration.
- Output: persisted ranking run, ranked assets, score, confidence metrics, outlier indicators, and source evidence.
- Replaceability: model code must be callable through a small service boundary so later approaches can replace the scoring internals without touching crawler, export, inspection, or API code.

### Confidence Context

MVP confidence should expose separate metrics rather than hide uncertainty behind a single opaque number:

- Number of trades involving the asset.
- Number of leagues represented.
- Recency-weighted signal volume.
- Whether signal is direct or inferred through trade bundles.
- Outlier contribution count.
- Add/drop baseline counts for replacement-level and near-zero assets.
- Format coverage fields where league settings, roster settings, and positional limits are available.

---

## Scalability & Performance

### Expected Load

- **Concurrent users:** One local operator for MVP.
- **Inspection traffic:** One local operator for CLI/CSV/query inspection.
- **Crawler load:** Bounded by configured users, leagues, API calls, and runtime.
- **Data growth:** Current-season Sleeper data at hobby/pilot scale; exact volume to be measured during early crawls.

### Scaling Strategy

- Start with single-process crawling and conservative request pacing.
- Use persisted frontier state before adding concurrency.
- Treat graph discovery and transaction sync as separate scalable loops, but do not prescribe a run cadence for MVP. MVP provides manual commands and durable state; scheduling is a later operational layer.
- After a league's initial transaction backfill is complete, rely on transaction deduplication and league-level high-watermarks so subsequent syncs do not behave like full historical recrawls.
- Support runtime rate adjustment before introducing crawler concurrency, because pacing control reduces risk while still allowing long crawls to be tuned.
- If crawling is too slow, introduce bounded async fetches inside the Sleeper client while preserving the same rate limiter and storage contracts.
- Move SQLite to Postgres only if database size, concurrent processes, or cloud execution make it necessary.
- Add scheduling after the manual CLI workflow proves useful; use free-tier cloud only if local execution is unreliable or impractical.

### Performance Targets

- Crawl progress visible within a few seconds of command start.
- Ranking inspection queries and CSV export complete fast enough for interactive local iteration on MVP-scale data.
- Ranking generation completes fast enough for repeated local iteration.
- Sleeper request rate defaults conservatively below documented guidance and remains operator-configurable during and between runs.

### Bottlenecks & Solutions

| Potential Bottleneck | Solution |
|----------------------|----------|
| Sleeper API rate limits or IP blocking | Conservative defaults, runtime-adjustable throttling, automatic slowdown, retry/backoff, raw progress visibility |
| Large graph expansion | Max users, max leagues, max API calls, max runtime, resumable frontier |
| Repeated recrawling | Fetched markers and upserts keyed by Sleeper IDs |
| Noisy rankings from sparse trades | Confidence metrics, stability comparisons, configurable model inputs later |
| Large ranking inspection output | Query filters, CSV slicing, and later server-side pagination if a web surface is added |

---

## Security & Reliability

### Security Architecture

- **Authentication:** None for MVP local use.
- **Authorization:** None for MVP local use.
- **Secrets/config:** Real seed username and local paths live in `.env` or ignored local config.
- **API security:** Read-only Sleeper API access with polite request behavior.
- **Data handling:** Store only public/read-only Sleeper data needed for crawling, ranking, and validation.

### Future Admin and Read Access

Future web/API access should distinguish privileged controls from read-only product surfaces:

- **Admin/control endpoints:** Must require authentication before they exist outside local-only development. This includes starting or resuming crawls, changing request rates, modifying config, triggering ranking runs, viewing operational errors, and managing exports.
- **Read-only rankings/trade views:** May eventually be public or lightly protected, depending on product direction. These surfaces can expose derived rankings, source trade evidence, and aggregate market context without granting operational control.
- **Default binding:** Any early FastAPI/admin adapter should bind to localhost by default and require explicit configuration before remote access.
- **Access separation:** Admin routes and read-only routes should be separable by router/module so auth can be enforced without entangling public ranking reads.

### Reliability

- Crawl runs should be resumable after process interruption.
- Frontier items should be idempotent enough to retry safely.
- Raw payloads should be stored before or alongside normalized facts where practical.
- Failures should be recorded in run metadata and frontier errors instead of only printed to the console.

### Disaster Recovery

- **Backup strategy:** Manual SQLite file copy for MVP.
- **Failover plan:** None for local MVP.
- **RTO:** Restore by using the latest SQLite copy or rerunning crawler.
- **RPO:** Acceptable to lose recent local crawl progress during MVP.

### Monitoring & Observability

- **Metrics:** Crawl counts, API calls, frontier depth, errors, trade counts, ranking asset counts.
- **Logs:** Structured console logs with run IDs and entity IDs.
- **Alerts:** None for MVP.
- **Tracing:** None for MVP.

---

## Deployment Architecture

### Environments

- **Development:** Local Python environment and SQLite database.
- **Test:** Local test database with fixtures and recorded sample payloads.
- **Production:** Not applicable for MVP; optional free-tier deployment only if crawler reliability requires it.

### Deployment Process

- **Build:** Package as a Python project with a CLI entrypoint.
- **Test:** Run unit tests for parsing, persistence, crawler state transitions, valuation, and inspection/query services.
- **Run:** Operator invokes CLI commands locally.
- **Inspection:** Operator uses CLI summaries, CSV exports, and direct query services; optional FastAPI adapter can be added if useful.
- **Rollback:** Revert code and use a copied SQLite database if needed.

### Infrastructure as Code

No IaC for MVP. If scheduled execution or free-tier cloud fallback becomes necessary later, add the smallest deployment recipe that supports the proven crawler workflow and the eventual admin/web surface.

---

## Risk & Mitigation

### Architectural Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Sleeper graph expands too broadly | Crawls become slow or noisy | Hard crawl limits, frontier visibility, current-season scope |
| SQLite schema becomes too coupled to model version one | Later ranking changes become hard | Preserve raw payloads and keep valuation behind service boundary |
| Disposable dashboard consumes MVP time | Slows validation and may be thrown away during web-app transition | Prefer CLI/CSV/query inspection; add only minimal FastAPI adapter if it directly supports the future API path |
| Draft-pick representation is incomplete | Dynasty rankings lose credibility | Store raw pick context and nullable precision rather than inventing exact values |
| Current-season trades are too sparse | Rankings may be unstable | Expose confidence/stability metrics and revisit historical season support later |
| Add/drop baseline is overinterpreted | Dropped players could be incorrectly treated as worthless | Use add/drop only to calibrate league rosterable-player lines and near-zero regions, not as normal trade constraints |
| Team roster context is hard to infer | Strong teams may drop players that weaker teams would roster, distorting baseline signals | Store roster context and treat drops from strong/deep rosters as weaker evidence |
| Manual-only MVP data gets stale | Rankings depend on operator remembering to rerun commands | Accept for MVP; add scheduling only after manual crawl/rank workflows prove useful |

### Technology Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| SQLAlchemy slows early development | More setup before first crawl | Keep schema focused and let planning split persistence work carefully |
| FastAPI added too early | UI/API scaffolding distracts from crawler and model validation | Defer routes until query/application services are useful enough to expose |
| Async crawling complexity appears too early | Harder debugging | Start single-process/sync; add bounded async only after measuring |
| External API payload shapes differ from assumptions | Parser failures or missing fields | Store raw payloads, make typed models tolerant where source data is optional |

---

## Decision Log

### Key Decisions Made

| Decision | Rationale | Alternatives |
|----------|-----------|--------------|
| Python-first implementation | Best fit for crawler, data modeling, and legacy lessons | TypeScript, Go |
| Local-first MVP | Keeps cost near zero and speeds validation | Hosted app from day one |
| SQLite persistence | Durable local storage without infrastructure | In-memory, Postgres, DuckDB |
| SQLAlchemy boundary | Keeps future Postgres path open | Raw SQLite, ORM-free scripts |
| Typer CLI | Clear local operator interface | argparse, Click |
| Application service boundary | Keeps CLI-first MVP modular enough for future web-app controls | Letting CLI commands own workflow logic |
| CLI/CSV/query inspection first | Avoids investing in a dashboard likely to be replaced by the real web app | FastAPI/Jinja dashboard, Streamlit, React |
| FastAPI deferred but kept as API path | Future admin/web surface can expose existing services when needed | Build FastAPI dashboard during MVP |
| SQLite-backed crawl frontier | Gives resumability without a message queue | In-memory queues, Redis/Celery |
| Current-season input for MVP | Keeps first model loop constrained | Historical multi-season crawl |
| Store raw facts plus normalized rows | Allows reprocessing without recrawling | Only normalized rows |
| Explainable replaceable valuation engine | Supports validation before sophistication | Complex ML from the start |

### Decisions Still Open

| Decision | Default for Planning | Revisit When |
|----------|----------------------|--------------|
| Exact package/dependency manager | Use the simplest repo-standard Python packaging choice during setup | Project scaffolding begins |
| Initial valuation algorithm details | Weighted trade-balance scoring with clear tests | First sample trade dataset exists |
| Rosterable-player line calculation | Start simple using league size, roster size, positional limits, and add/drop frequency | Enough add/drop samples exist to compare league archetypes |
| Add/drop segmentation | Segment by player position and comparable league/roster settings where possible | Baseline calibration appears noisy across league types |
| Team context weighting | Store roster context first; use conservative weighting until roster-strength metrics are validated | Drops from strong rosters appear to distort lower-end values |
| Web/admin inspection surface | Defer implementation; likely expose crawl start/status, ranking run, ranking read, evidence read, and export download first | CLI/query workflows are validated |
| FastAPI/admin activation trigger | Defer routes until CLI/query services are stable | Need remote control, authenticated admin workflows, or real web-app integration |
| Cloud fallback platform | Defer | Local crawling proves unreliable |

---

## Phase Gate

- **Ready to move to Planning & Decomposition?** [x] Yes
- **Remaining concerns:** Final valuation algorithm details should be settled after the first persisted sample of completed trades. Cloud fallback remains intentionally deferred.
- **Owner decision:** Approved by John. Architecture is ready to hand off to Planning & Decomposition.

---

*Save this document and diagrams in your project repo for future reference.*
