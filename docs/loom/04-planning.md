# Planning & Decomposition

Turn the Trade Winds architecture into an executable implementation plan.

**Project Name:** trade-winds  
**Date:** 2026-05-14  
**Planning Lead:** Codex + John Hightshue

---

## Scope

### Planning Scope

This plan covers the Trade Winds MVP: a local-first Python CLI system that starts from a configured Sleeper username, discovers current-season Sleeper users/leagues, persists league and transaction facts in SQLite, generates dynasty-oriented player and draft-pick rankings from completed trades, and exposes results through CLI, CSV, and direct query inspection.

The plan intentionally excludes a primary dashboard, public API, auth/account system, paid infrastructure, scheduled production operation, redraft-specific ranking work, historical multi-season crawling, and complex ML ranking approaches.

### Inputs

- Discovery document: `docs/loom/01-discovery.md`
- Requirements document: `docs/loom/02-requirements.md`
- Architecture document: `docs/loom/03-architecture.md`
- Architecture planning inputs: `docs/loom/03-architecture.md#planning-inputs`

### Decisions Made

- Use `uv` with `pyproject.toml` for Python project, dependency, virtual environment, lockfile, and command execution workflow.
- Keep valuation algorithms interchangeable: crawlers and normalizers store stable facts, ranking runs record model/config metadata, and future models should be able to read the same persisted facts without recrawling or rewriting storage.
- Start with a simple, explainable model v1 rather than a complex solver, as long as the model boundary remains replaceable.
- Defer FastAPI for MVP implementation. Preserve application/query service boundaries so a local admin/read API can be added later without rewriting crawler, ranking, export, or inspection logic.
- Use an MVP inspection surface of `inspect runs`, `inspect rankings`, `inspect asset`, `inspect compare`, and `export rankings`.
- Start with single-process synchronous crawling and a shared rate limiter. Add bounded async fetching later only if measured crawl speed becomes an MVP bottleneck.

### Open Decisions

- Type checker choice remains open for CI bootstrap: Pyright versus mypy.
- `pytest-httpx` versus `respx` remains open until Sleeper client implementation.
- CI blocking promotion timing remains open until the first implementation slice makes the intentionally red suite collect and pass.
- Real Sleeper payload edge cases may require new fixtures, but existing test rewrites require explicit approval under `docs/loom/05-contracts-tests-cicd.md`.

### Architecture Handoff Summary

- **Components / modules to build:** `config`, `app`, `cli`, `sleeper`, `db`, `repositories`, `crawl`, `transactions`, `valuation`, `inspection`, `exports`, and test-support modules.
- **Likely workstreams:** Project foundation, service boundary design, persistence/schema, Sleeper client, crawl orchestration, transaction normalization, valuation, export/inspection, tests/contracts, and CI/CD bootstrap.
- **Critical sequencing constraints:** Scaffold/config before app context; schema contract before database implementation; database before crawl/ranking persistence; Sleeper client before live crawl; transaction facts before ranking; ranking outputs before export/inspection.
- **Parallelization opportunities:** Sleeper client contracts and persistence contracts can be refined independently; valuation fixture design can proceed once asset identity is locked; export/inspection contracts can proceed once ranking output schema is stable.
- **Contracts, schemas, or interfaces needing tests:** Settings/app context, CLI commands/options, Sleeper endpoints, retry/rate limiting, database schema, repositories, crawl frontier/fetched markers, transaction normalizer, valuation model/confidence/outliers, export/inspection queries, and fixture workflow.
- **Service/module boundaries to preserve:** CLI stays thin; application services coordinate reusable workflows; Sleeper client has no persistence writes; repositories own SQLAlchemy; valuation reads persisted facts and never calls Sleeper; export/inspection do not recalculate rankings.
- **Highest-risk areas to isolate early:** Schema/idempotency, Sleeper payload variance, draft-pick identity, add/drop baseline interpretation, crawl resumability, and valuation explainability.
- **Decisions Planning must not reopen without new evidence:** Local-first MVP, current-season scope, CLI/CSV/query inspection first, FastAPI deferred, completed trades as primary ranking signal, add/drop as baseline signal, raw-plus-normalized persistence.

---

## Work Breakdown

### Workstreams

| Workstream | Purpose | Owner | Scope | Notes |
|------------|---------|-------|-------|-------|
| Project Foundation | Establish the Python app skeleton, dependency management, config loading, and CLI entry point | Codex | Python package, Typer CLI, config module, ignored local data/output paths, developer commands | Must happen first because every other workstream needs the app shell |
| Service Boundary Design | Keep implementation aligned with architecture diagrams and class/service contracts | Codex | `AppContext`, application services, repository boundaries, service/class map updates | Should be checked as modules are created, not only after implementation |
| Persistence & Schema | Create the SQLite persistence boundary and migrations | Codex | SQLAlchemy models, Alembic setup, repository/session helpers, tables from architecture | Schema should favor raw fact preservation and idempotent upserts |
| Sleeper Client | Encapsulate Sleeper API access and polite HTTP behavior | Codex | `httpx` client, endpoint methods, retries/backoff, throttling, typed parsing, raw response capture | Keep rate control outside CLI so future services reuse it |
| Crawl Orchestration | Discover users/leagues and sync transactions with durable state | Codex | Frontier processing, fetched markers, crawl runs, league sync state, discovery command, transaction command | Start single-process; add concurrency only after a measured need |
| Transaction Normalization | Convert Sleeper payloads into stable trade/add/drop facts | Codex | Transactions, transaction assets, trade sides/assets, draft-pick representation, raw payload retention | Preserve odd trades and derive outlier status later |
| Valuation Engine | Generate explainable rankings from persisted facts | Codex | Model v1, recency weighting, add/drop baseline hooks, confidence metrics, outlier indicators, ranking run persistence | Completed trades are primary; add/drops are conservative baseline signals |
| Export & Inspection | Make outputs inspectable without a dashboard | Codex | CSV export, CLI summaries, ranking inspection, source evidence inspection, run comparison | This is the main MVP validation surface |
| Tests & Contracts | Lock behavior around API parsing, schema, crawl resumability, and ranking output | Codex | Unit tests, fixture payloads, CLI smoke tests, database migration checks | Formalized in next Loom phase, but planned here for sequencing |
| CI/CD Bootstrap | Make local checks reproducible in GitHub Actions | Codex | GitHub Actions workflow, `uv.lock`, required checks, non-live test policy | Separate bootstrap slice before merge-gated implementation |
| Optional Web/API Adapter | Preserve or add a thin future API path | Codex | FastAPI adapter only if needed, localhost-only defaults, routes over existing services | Not required for MVP delivery |

### Implementation Slices

| Slice | Outcome | Depends On | Priority |
|-------|---------|------------|----------|
| S0: Scaffold | Repo can install/run a `trade-winds` CLI with help output | None | Must |
| S1: Config & App Context | CLI resolves local config, database path, season, seed username, request rate, and crawl limits | S0 | Must |
| S1.5: Service Boundaries | Initial modules match the architecture service/class map and dependency rules | S0, S1 | Must |
| S1.75: Schema Contract Lock | Architecture and tests define exact initial tables, constraints, repository responsibilities, and idempotency keys | S0, S1.5 | Must |
| S1.9: CI Bootstrap | GitHub Actions workflow, locked dependencies, local command parity, and documented required checks exist | S0, S1.75 | Must before merge-gated implementation |
| S2: Database Foundation | Alembic migrations create core tables and repositories can open SQLite sessions | S0, S1, S1.75, S1.9 | Must |
| S3: Sleeper Client | Client can fetch seed user, leagues, league users, rosters, transactions, traded picks, and player metadata with retries/rate limiting | S1 | Must |
| S4: Discovery Crawl | `crawl discover` persists users, leagues, league users, rosters, frontier state, fetched markers, and crawl run metadata | S2, S3 | Must |
| S5: Transaction Sync | `crawl transactions` persists current-season transactions, add/drop movement, trade sides/assets, draft picks, league sync state, and raw payloads | S2, S3, S4 | Must |
| S6: First Ranking Run | `rank` reads persisted completed trades and writes ranking runs/assets/evidence | S5 | Must |
| S7: CSV Export | `export` writes stable ranking CSV files from persisted ranking runs | S6 | Must |
| S8: CLI Inspection | `inspect` shows ranking rows, run metadata, source trades/evidence, and basic filters | S6 | Must |
| S9: Stability Comparison | Repeated ranking runs can be compared for movement and unstable assets | S6, S8 | Should |
| S10: Optional Adapter | Minimal FastAPI read/admin adapter exists over app/query services if useful | S6, S8 | Could |

---

## Ownership Boundaries

### Ownership Map

| Owner | Files/Modules/Services | Responsibilities | Out of Scope |
|-------|------------------------|------------------|--------------|
| Project Foundation | `pyproject.toml`, package root, CLI bootstrap, app context | Dependency setup, command registration, config loading, local paths | Domain logic, Sleeper normalization, valuation details |
| Service Boundary Design | `app/`, application service interfaces, architecture diagrams | Composition root, dependency direction, service/class map alignment | Business logic implementation details |
| Persistence | `db/`, `models/`, `repositories/`, `migrations/` | Schema, sessions, migrations, idempotent upserts, query helpers | HTTP calls, CLI rendering, ranking math |
| Sleeper Client | `sleeper/` | Endpoint methods, rate limiting, retries, typed API-boundary models | Database writes, crawl queue decisions, valuation |
| Crawl | `crawl/`, crawl application service | Discovery traversal, transaction sync workflow, frontier and run state updates | Ranking, CSV formatting, future web routing |
| Normalization | `transactions/` or crawl normalizer modules | Transaction asset movement, trade projections, draft pick normalization | Model scoring, endpoint transport |
| Valuation | `valuation/`, ranking application service | Model v1, confidence metrics, outlier indicators, ranking persistence | Raw crawl fetching, schema migrations |
| Inspection/Export | `inspection/`, `exports/`, CLI renderers | CSV output, CLI summaries, filters, evidence views, run comparison | Crawl mutation and model internals |
| Tests | `tests/`, fixtures | Fixture design, behavior locks, command smoke tests | Production scheduling or hosted deployment |

### Shared Areas

| Shared Area | Owners | Coordination Rule |
|-------------|--------|-------------------|
| Application service contracts | Foundation, Crawl, Valuation, Export/Inspection | Services should accept config/session/client dependencies explicitly and avoid importing CLI modules |
| Component internal contracts | All workstreams | `docs/loom/03-architecture.md` is the source for component inputs, outputs, responsibilities, and test targets; update architecture before changing these boundaries materially |
| Database schema | Persistence, Crawl, Valuation, Inspection | Schema changes require migration plus repository/query updates in the same slice |
| Asset identity format | Normalization, Valuation, Export/Inspection | Define one stable asset key convention before ranking/export work starts |
| Raw payload shape | Sleeper Client, Persistence, Normalization | Store raw JSON snapshots, but query normalized columns for application behavior |
| CLI command names/options | Foundation, Crawl, Valuation, Inspection | Keep initial command contract close to architecture unless implementation reveals a simpler shape |

### Boundary / Contract Alignment

- **Source architecture sections:** `Initial Service and Class Map`, `Component Internal Contracts`, `Dependency Rules`, `Initial CLI Commands`, `Initial Schema Contract`, `Valuation Architecture`, and `Planning Inputs` in `docs/loom/03-architecture.md`.
- **Dependency rules:** CLI and future API surfaces call application/query services; domain services do not import CLI/FastAPI; Sleeper client does not write to SQLite; repositories own SQLAlchemy; valuation does not call Sleeper; export/inspection do not mutate source facts.
- **Interfaces / schemas / commands to keep stable:** `Settings.load`, `AppContext.create`, Sleeper endpoint methods, repository bundle responsibilities, `CrawlApplicationService`, `RankingApplicationService`, `RankingQueryService`, `CsvExporter`, asset key format, database schema contract, and `trade-winds crawl/rank/export/inspect` command names.
- **Architecture updates required before changing:** Database table/key contract, asset identity format, service dependency direction, valuation source-of-truth rules, CLI inspection surface, or FastAPI/dashboard deferral.

---

## Dependencies & Sequencing

### Dependency Graph

1. Project scaffold and config.
2. Service boundaries and `AppContext`.
3. Schema contract lock.
4. CI bootstrap.
5. Database foundation and migrations.
6. Sleeper client.
7. Discovery crawl.
8. Transaction sync and normalization.
9. Ranking engine.
10. CSV export and CLI inspection.
11. Stability comparison.
12. Optional FastAPI/web adapter.

### Critical Path

The critical path is persistence-backed crawling into persisted transaction facts, then ranking generation from those persisted facts. Nothing meaningfully validates the product until a real crawl can produce completed trades and a ranking run can be regenerated without calling Sleeper.

The first implementation should therefore focus on:

1. A runnable CLI and local config.
2. A locked initial SQLite schema contract.
3. A CI workflow that can run the same local checks.
4. A durable SQLite schema that satisfies that contract.
5. A Sleeper client with conservative request behavior.
6. Discovery plus transaction sync with resumable state.
7. Ranking from persisted data only.
8. CSV/CLI inspection.

### Parallel Work

| Workstream | Can Start When | Integration Point |
|------------|----------------|-------------------|
| Sleeper Client | After config shape is known | Crawl orchestrator calls endpoint methods |
| Persistence | After package scaffold is chosen | Crawl and ranking services depend on repositories |
| Valuation Design | After asset identity convention is drafted | Ranking service reads normalized trade facts |
| Export/Inspection | After ranking output schema is stable | CLI commands query ranking runs/assets/evidence |
| Tests/Fixtures | As each slice lands | Fixture payloads lock parsing, normalization, and ranking behavior |

---

## Agent Context Packets

### Context Packet: Project Foundation

- **Owner:** Codex
- **Goal:** Create the runnable Python application shell.
- **Relevant requirements:** Configure a crawl; CLI outputs; local-first MVP.
- **Relevant architecture decisions:** Python 3.12+, Typer CLI, CLI as thin wrapper over application services.
- **Owned files/services/modules:** Project metadata, package root, CLI bootstrap, config/app context modules.
- **Contracts to preserve:** Application services must not import CLI modules; local operator values must not be committed.
- **Risks and assumptions:** Dependency manager choice affects commands and CI setup.
- **Expected output:** Runnable `trade-winds --help`, config loading, ignored local data/output directories.
- **Handoff notes required:** Setup commands, config keys, command entry points, any dependency choices.

### Context Packet: CI Bootstrap

- **Owner:** Codex
- **Goal:** Make the local TDD checks reproducible in GitHub Actions before implementation branches rely on them.
- **Relevant requirements:** Tests/contracts-first workflow; local-first MVP; no hosted deployment required.
- **Relevant architecture decisions:** `uv` project workflow, pytest, Ruff, optional type checking, Alembic migration checks.
- **Owned files/services/modules:** `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock`, CI notes in `docs/loom/05-contracts-tests-cicd.md`.
- **Contracts to preserve:** CI must not call live Sleeper APIs by default; CI commands must match documented local commands; red tests are allowed during contract-writing work but required checks become enforced once the first implementation slice is expected to pass.
- **Risks and assumptions:** Enforcing CI too early can block intentional red-test commits; delaying CI too long can let local-only assumptions creep in.
- **Expected output:** A CI workflow that installs Python, installs `uv`, runs lockfile/dependency checks, Ruff format/lint, pytest, coverage after package scaffold, and migration checks after Alembic exists.
- **Handoff notes required:** Required checks, when each check becomes blocking, secrets policy for live smoke tests, and any skipped checks.

### Context Packet: Persistence & Schema

- **Owner:** Codex
- **Goal:** Lock and implement durable SQLite storage for crawl state, facts, and ranking outputs.
- **Relevant requirements:** SQLite persistence, resumable crawl, raw fact preservation, ranking run storage.
- **Relevant architecture decisions:** SQLAlchemy 2.x, Alembic, normalized facts plus JSON raw snapshots.
- **Owned files/services/modules:** Database models, migrations, session helpers, repositories.
- **Contracts to preserve:** Stable Sleeper IDs, idempotent upserts, nullable precision for unknown draft pick positions, raw payload columns, ranking run reproducibility, explicit crawl state transitions.
- **Risks and assumptions:** Over-modeling early can slow implementation; under-modeling can make ranking queries painful.
- **Expected output:** Executable schema contract test, initial migration, repository helpers for users, leagues, rosters, transactions, crawl state, rankings.
- **Handoff notes required:** Table names, primary keys, uniqueness/idempotency constraints, migration commands, known schema compromises.

### Context Packet: Sleeper Client

- **Owner:** Codex
- **Goal:** Wrap Sleeper API access behind typed, throttled endpoint methods.
- **Relevant requirements:** Sleeper client, polite crawler behavior, retries/backoff, raw payload capture.
- **Relevant architecture decisions:** `httpx`, Pydantic at the boundary, configurable request rate below Sleeper guidance.
- **Owned files/services/modules:** Sleeper client, endpoint models, rate limiter/retry helpers.
- **Contracts to preserve:** Client returns payloads that can be persisted raw and normalized downstream.
- **Risks and assumptions:** Sleeper payload variance may require permissive parsing and raw JSON fallback.
- **Expected output:** Endpoint methods for seed user, user leagues, league users, rosters, transactions, traded picks, players.
- **Handoff notes required:** Endpoint coverage, retry behavior, rate-limit settings, any undocumented payload quirks.

### Context Packet: Crawl & Normalization

- **Owner:** Codex
- **Goal:** Build resumable discovery and transaction sync workflows.
- **Relevant requirements:** Manual CLI crawler, expandable graph crawl, current-season trade collection, add/drop capture.
- **Relevant architecture decisions:** `crawl_frontier`, `fetched_markers`, `crawl_runs`, `league_sync_state`, raw plus normalized transaction facts.
- **Owned files/services/modules:** Crawl services, frontier processing, transaction sync, transaction normalizers.
- **Contracts to preserve:** Re-running a crawl should not duplicate facts; interrupted frontier items should be retryable.
- **Risks and assumptions:** Graph expansion can grow quickly; limits must be enforced from the beginning.
- **Expected output:** `crawl discover` and `crawl transactions` commands backed by reusable services.
- **Handoff notes required:** Resume behavior, stopping-limit behavior, counters recorded, known failed payload cases.

### Context Packet: Valuation Engine

- **Owner:** Codex
- **Goal:** Produce explainable dynasty rankings from persisted completed trades.
- **Relevant requirements:** Completed trades as primary signal, recency weighting, player/pick outputs, confidence/sample context, outlier flags.
- **Relevant architecture decisions:** Model isolated behind a service boundary; add/drops used conservatively for baseline calibration.
- **Owned files/services/modules:** Valuation model, ranking service, ranking persistence, evidence generation.
- **Contracts to preserve:** Ranking must read persisted facts only; output must be reproducible from stored run config and source facts.
- **Risks and assumptions:** Sparse trades can produce noisy scores; confidence context must make uncertainty visible.
- **Expected output:** `rank` command creates persisted ranking runs/assets/evidence.
- **Handoff notes required:** Model version, scoring explanation, confidence fields, limitations and next model candidates.

### Context Packet: Export & Inspection

- **Owner:** Codex
- **Goal:** Make rankings and source evidence easy to inspect without a dashboard.
- **Relevant requirements:** CSV export, concise CLI summary, ranking inspection, source-trade drilldown, stability comparison.
- **Relevant architecture decisions:** CSV and CLI/query inspection are the MVP surfaces.
- **Owned files/services/modules:** Exporter, inspection query services, CLI renderers.
- **Contracts to preserve:** Stable CSV column names; commands read persisted ranking outputs.
- **Risks and assumptions:** Inspection can become too broad; keep first commands tied to ranking credibility.
- **Expected output:** `export`, `inspect rankings`, `inspect asset`, and basic run comparison.
- **Handoff notes required:** CSV path conventions, columns, filter options, example commands.

---

## Integration Plan

### Checkpoints

| Checkpoint | Purpose | Required Evidence | Owner |
|------------|---------|-------------------|-------|
| C0: CLI Boot | Confirm the app shell is runnable | `trade-winds --help` works; config errors are readable | Project Foundation |
| C0.5: Boundary Map | Confirm implementation follows architecture diagrams | `AppContext`, application service, repository, client, and domain module dependencies match the service/class map | Service Boundary Design |
| C0.75: Schema Contract Locked | Confirm previous phases provide enough persistence detail for TDD | `docs/loom/03-architecture.md` names tables, keys, JSON columns, and idempotency constraints; `tests/contracts/test_database_schema_contract.py` exists and fails until implemented | Persistence/Tests |
| C0.9: CI Bootstrap Ready | Confirm CI can reproduce local checks | `.github/workflows/ci.yml` exists, `uv.lock` exists, CI avoids live Sleeper calls by default, and required checks are documented | Project Foundation/Tests |
| C1: Schema Ready | Confirm durable storage can be created and migrated | Fresh SQLite database migrates successfully; core tables, keys, constraints, and raw JSON columns satisfy the schema contract | Persistence |
| C2: API Smoke | Confirm Sleeper calls work against a configured seed | Seed user and at least one league can be fetched with throttling | Sleeper Client |
| C3: Discovery Resume | Confirm graph discovery is durable | Discovery run persists users/leagues/frontier and can resume without duplicating rows | Crawl |
| C4: Transaction Facts | Confirm completed trades and add/drops are stored | Known league transaction payloads produce normalized transactions/assets/trade sides | Crawl/Normalization |
| C5: Ranking Run | Confirm rankings come from persisted data | `rank` creates ranking run/assets/evidence without live API calls | Valuation |
| C6: Inspection Loop | Confirm John can judge output credibility | CSV export and CLI inspection show ranks, samples, leagues, recency, and source evidence | Export/Inspection |
| C7: Stability Check | Confirm repeated runs can be compared | Two ranking runs produce movement comparison or unstable-asset output | Export/Inspection |

### Conflict Resolution

Schema and asset identity are the two places most likely to create cascading changes. If implementation reveals a needed schema or asset-key change, update the migration/model/repository, ranking code, export code, and planning notes in the same pass. Avoid preserving a bad early contract just because downstream code already exists.

When implementation deviates from architecture, record the reason in `docs/loom/06-implementation.md` rather than silently drifting.

### Escalation Path

Stop and ask for direction if:

- Sleeper API behavior makes username-seeded discovery impractical.
- Current-season trade volume is too sparse to validate rankings.
- The schema needs to drop a major architecture requirement rather than defer it.
- Ranking output needs an external prior to produce usable results.
- Local crawling appears likely to violate polite API usage even with conservative throttling.

### Contract / Test Candidates

These candidates are carried into `docs/loom/05-contracts-tests-cicd.md` and executable tests.

| Candidate | Source | Why it matters | Suggested test shape |
|-----------|--------|----------------|----------------------|
| Config and app context contracts | Architecture runtime composition | Every service depends on stable configuration and wiring | Unit/contract tests for `Settings.load` and `AppContext.create` |
| CLI command contract | Architecture initial CLI commands | CLI is the MVP operator surface | Typer CLI tests for help, missing config, options, and command dispatch |
| Schema contract | Architecture data design | Crawl resumability and ranking reproducibility depend on durable state | SQLAlchemy inspection contract and Alembic migration tests |
| Repository idempotency | Planning persistence ownership | Re-running crawls/syncs must not duplicate facts | Temp SQLite repository contract tests |
| Sleeper endpoint coverage | Architecture integration points | External API payloads are a major risk | Fixture-backed client contract tests and opt-in live smoke test |
| Rate limiter/retry policy | Requirements polite API behavior | Avoid API stress and make failures predictable | Fake-clock unit tests and retry policy unit tests |
| Crawl discovery resume | Requirements resumable crawl | Interrupted crawls should safely resume | Integration test with fake Sleeper client and temp DB |
| Transaction normalization | Architecture transaction sync flow | Rankings depend on stable trade/add/drop facts | Fixture-backed unit tests for trades, add/drops, picks, and odd trades |
| Asset identity | Shared architecture contract | Normalization, ranking, export, and inspection must agree on keys | Unit tests for player and pick asset keys |
| Valuation model v1 | Valuation architecture | Ranking credibility depends on deterministic explainable behavior | Fixture-backed unit tests with exact expected outputs and recency behavior |
| Confidence/outliers | Requirements credibility context | Outputs should expose uncertainty and preserve weird trades | Unit tests for calculators and outlier flags |
| Export/inspection | Requirements inspectable MVP | John needs CSV and query/CLI evidence workflows | CLI/query/export tests seeded from persisted ranking data |
| Full fixture workflow | Integration checkpoints | Confirms MVP loop without live APIs | End-to-end integration test over fake Sleeper data and temp DB |
| CI bootstrap | Planning S1.9 | Local and future PR checks need parity | Documented workflow plan and later `.github/workflows/ci.yml` |

---

## Delivery Plan

### Milestones

| Milestone | Outcome | Workstreams Included | Exit Criteria |
|-----------|---------|----------------------|---------------|
| M1: Local Shell | Runnable CLI with config and database setup | Project Foundation, Persistence | CLI runs, config loads, migrations create SQLite DB |
| M2: Crawled Facts | Local crawl persists users, leagues, rosters, transactions, trade facts, and add/drop movement | Sleeper Client, Crawl, Normalization | Discovery and transaction sync can be resumed and queried |
| M3: First Rankings | Persisted completed trades generate rankings and evidence | Valuation, Persistence | `rank` writes ranking run/assets/evidence with confidence context |
| M4: Inspection MVP | Rankings can be inspected through CSV, CLI, and direct queries | Export/Inspection | John can review top assets, filter/slice outputs, and inspect source trades |
| M5: Validation Loop | Ranking stability and model credibility can be evaluated | Valuation, Export/Inspection, Tests | Repeated runs can be compared and noisy assets identified |

### Initial Sequential Plan

1. Scaffold Python package, Typer CLI, config loader, and ignored local paths.
2. Lock the initial schema contract in architecture and executable tests.
3. Bootstrap CI/CD with non-live checks and dependency lockfile once the scaffold can install.
4. Add SQLAlchemy/Alembic and create the initial schema.
5. Implement Sleeper client with throttling/retries and endpoint smoke tests.
6. Build `crawl discover` with persisted frontier, run metadata, users, leagues, league users, and rosters.
7. Build `crawl transactions` with league sync state, transaction normalization, completed trades, add/drop assets, and draft-pick handling.
8. Implement model v1 as a simple, explainable ranking service over persisted trade facts.
9. Persist ranking runs, ranking assets, and ranking evidence.
10. Add CSV export and concise CLI ranking summary.
11. Add inspection commands for rankings, run metadata, source evidence, and movement comparison.
12. Use real crawl/ranking outputs to decide whether to deepen valuation, add tests, or introduce optional FastAPI.

### Later Agile Cycles

After the first full crawl/rank/export/inspect loop works, iterate in small validation cycles:

- Improve transaction normalization based on real payload edge cases.
- Tune recency weighting and confidence metrics.
- Add or adjust outlier flags after inspecting strange trades.
- Add richer source-evidence views for assets with surprising ranks.
- Compare repeated runs and small configuration changes for stability.
- Introduce historical seasons or lookback windows only if current-season data is too sparse.
- Consider FastAPI/admin/web access only after query services feel durable.

---

## Update Policy

Use Planning as the implementation coordination map. Update this document when architecture decisions change, workstream ownership changes, contract boundaries move, or real implementation findings force a better slice order. Do not silently drift from architecture; record material deviations in the relevant phase doc and request approval when a locked contract or test must change.

---

## Phase Gate

- **Ready to move to Contracts & Tests / CI/CD?** [x] Yes [ ] No
- **Remaining concerns:**
  - The baseline valuation algorithm still needs a concrete contract and fixture-driven expected outputs before valuation implementation.
  - Sleeper transaction payload edge cases need representative fixtures before transaction-normalization implementation.
  - The project scaffold and dependency manager choice should be made before test/CI commands are finalized.
  - CSV columns and CLI inspection command names should be treated as contracts before export/inspection implementation.
  - Initial schema details must be locked in architecture and executable schema tests before database implementation.
  - CI/CD is not set up yet; it should become its own bootstrap slice after package scaffold and lockfile generation, before merge-gated implementation work.
- **Owner decision:** Proceed to Contracts & Tests / CI/CD planning, but do not start database/crawl/ranking implementation until missing schema, repository, endpoint, valuation, and CI bootstrap contracts are converted into failing tests or documented checks.

---

*This document is the implementation coordination map. Update it when architecture decisions change, when workstream ownership changes, or when real Sleeper payloads force a better slice order.*
