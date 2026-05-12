# Requirements

Define and document requirements for the Trade Winds MVP.

**Project Name:** trade-winds
**Date:** 2026-05-12
**Requirements Lead:** Codex + John Hightshue

---

## Overview

### Discovery Inputs

- **Core problem:** Trade Winds needs to regularly crawl Sleeper users, leagues, and completed trades, then use those accepted trades as weighted market signals for relative player and draft-pick valuations.
- **Primary user / operator:** John Hightshue as project owner, builder-analyst, and first operator.
- **Future / external users:** Fantasy football managers who want understandable, directionally trustworthy trade and player valuation signals.
- **Working shape:** A local-first data engine and analysis tool with resumable crawling, persisted market facts, valuation generation, CSV/CLI outputs, and a thin dashboard for inspection.
- **First useful version:** Prove the data and model before investing in public product polish.
- **Explicitly out of scope:** Public API, auth/accounts, paid infrastructure, production hardening, complex ML, redraft optimization, and perfect league-format segmentation.
- **Success / validation signals:** Repeatable crawl, persisted users/leagues/trades, generated rankings, stable outputs across runs, readable dashboard, and near-zero cost.
- **Open questions carried forward:** Concrete stack choices, cloud fallback shape, and whether any legacy implementation ideas should be reused.

### Solution Vision

Trade Winds MVP is a local-first dynasty fantasy football market intelligence system. It starts from a configured Sleeper username, crawls the nearby Sleeper user-league graph, persists discovered entities and completed trades, and turns those trades into time-weighted relative valuations for players and draft picks.

The first product surface is intentionally inspectable rather than polished: a CSV export, a concise CLI summary, and a lightweight rankings dashboard. The MVP should help John answer the central validation question: do completed Sleeper trades produce rankings that are stable, explainable, and useful enough to justify deeper product work?

---

## Scope Definition

### In Scope

- [x] Local configuration for operator-specific values such as the initial Sleeper username, request limits, and future trade lookback window.
- [x] Sleeper API client for users, leagues, league rosters/users, transactions/trades, traded draft picks, and player metadata.
- [x] Manual CLI command to run the crawler.
- [x] Expandable graph crawl from the initial Sleeper username, with configurable stopping limits such as max users, max leagues, max API calls, and runtime.
- [x] Current-season-only trade collection and ranking input for MVP.
- [x] Resumable crawl state including crawl frontier, fetched markers, run metadata, timestamps, counts, and errors.
- [x] SQLite persistence for users, leagues, league settings, rosters or relevant roster context, completed trades, trade assets, draft picks, player metadata snapshots, crawl runs, and ranking outputs.
- [x] Configurable request throttling below Sleeper's documented guidance, plus retries with backoff and progress logging.
- [x] Dynasty-first valuation model using completed trades as primary market facts.
- [x] Simple, explainable baseline valuation model with a replaceable boundary for later model improvements.
- [x] Recency weighting for trade signals.
- [x] Player and draft-pick valuation outputs.
- [x] Basic confidence/sample context for rankings.
- [x] Outlier flagging for unusual trades while preserving raw completed trades.
- [x] CSV export for generated rankings.
- [x] Concise CLI summary after crawl/ranking runs.
- [x] Lightweight dashboard focused on rankings inspection.
- [x] Basic dashboard filters for asset type and position, with a path for later league-format splits.
- [x] Basic source-trade evidence drilldown from rankings to the trades contributing to an asset's valuation.
- [x] Optional free-tier cloud fallback if local crawling is unreliable, too slow, hard to schedule, or affected by local network/API friction.
- [x] Bounded legacy implementation review before final architecture decisions.

### Out of Scope

- Public API.
- Account system, authentication, or user-specific web sessions.
- Paid hosting, managed databases, or other recurring infrastructure cost.
- Production-grade deployment, monitoring, or alerting.
- Remote dashboard access as a primary MVP requirement.
- Complex ML or opaque ranking algorithms before a simple trade-derived model is validated.
- Redraft-specific rankings.
- Full support for every league scoring format in the first rankings output.
- Historical season crawling and multi-season valuation inputs.
- Manual exclusion tooling for trades, unless validation proves it is needed.
- Treating KeepTradeCut or another rankings site as ground truth.
- Scraping or collection approaches that violate Sleeper's public API expectations.

### MVP

The MVP is complete when John can run a local command that starts from a locally configured Sleeper username, crawls and persists current-season Sleeper users/leagues/completed trades with resumable state, generates dynasty-oriented player and draft-pick rankings from time-weighted completed trades, and inspects those rankings through CSV, CLI output, and a thin dashboard table.

MVP output must include enough context to judge credibility: sample counts, league coverage where available, recency context, direct versus inferred signal if applicable, visible outlier flags, and enough model explanation to understand why an asset is ranked where it is.

### Phased Releases

- **Phase 1: Local Data Foundation**
  Manual CLI crawler, local config, Sleeper API client, expandable crawl frontier, SQLite schema, resumable crawl runs, player metadata snapshots, and raw completed-trade persistence.
- **Phase 2: First Valuation Loop**
  Trade asset normalization, player/pick valuation model, recency weighting, confidence/sample metrics, outlier flags, CSV export, and CLI summary.
- **Phase 3: Inspection Dashboard**
  Lightweight rankings table with filters, confidence context, and links or views that make source trade evidence inspectable.
- **Phase 4: Automation / Fallback**
  Local scheduled execution first, with optional free-tier cloud worker/dashboard only if local crawling is unreliable.

### Optional / Not Needed Yet

| Item | Status | Why not now? | Revisit when |
|------|--------|--------------|--------------|
| Public API | Deferred | Rankings need to prove useful before productizing access | Rankings are credible and external consumers are clear |
| Auth/accounts | Deferred | MVP is operator-focused and local-first | Multiple users need personalized access |
| Historical season crawling | Deferred | Current-season scope keeps the first crawl/model loop smaller | Current-season data is too sparse or rankings need historical stability checks |
| Active lookback-window filtering | Deferred | The config shape exists, but MVP uses current-season trades only | Historical or multi-window ranking work begins |
| Redraft rankings | Deferred | Dynasty is the first useful format and drives pick valuation | Dynasty baseline is credible |
| Manual trade exclusion tooling | Deferred | MVP should preserve completed trades and flag outliers first | Specific outliers demonstrably distort outputs |
| Remote dashboard access | Optional | Not a cloud fallback trigger for MVP | Cloud fallback makes remote access cheap |
| Complex ML ranking model | Deferred | First model should be explainable and inspectable | Simple model limitations are understood from source evidence |

---

## Functional Requirements

### User Stories

#### Story 1: Configure a Crawl

As John, I want to configure the seed Sleeper username, request rate, local database path, and future lookback-window shape so that the crawler can run repeatably without committing personal or environment-specific values.

Acceptance Criteria:

- The real seed username is read from environment variables or ignored local config.
- The lookback-window configuration shape exists for future historical or multi-window ranking work, but MVP ranking inputs are current-season only.
- Request-rate settings are configurable and default below Sleeper's published guidance.
- Missing required config produces a clear CLI error.

#### Story 2: Run a Resumable Sleeper Crawl

As John, I want to run a manual CLI crawl so that Trade Winds can discover users, leagues, and completed trades from Sleeper.

Acceptance Criteria:

- A CLI command starts a crawl from the configured Sleeper username.
- The crawler expands outward through discovered users and leagues until configured stopping limits are reached.
- The system discovers and persists users, leagues, league settings, and current-season completed trades.
- Historical seasons are not included in MVP crawl/ranking inputs unless a later requirement explicitly expands scope.
- The system records crawl run status, counts, timestamps, and errors.
- Interrupted crawls can resume without refetching everything from scratch.
- API calls are throttled and retried with backoff on transient failures.

#### Story 3: Store Completed Trade Facts

As John, I want completed trades stored faithfully so that model iterations can be rerun without losing the original market facts.

Acceptance Criteria:

- Completed trades are stored with Sleeper IDs, league references, transaction timestamps, participating rosters/users where available, and raw payload references or snapshots.
- Player assets use Sleeper player IDs.
- Draft-pick assets preserve season, round, original owner/current owner context, and exact pick position only when known.
- Strange completed trades are stored rather than discarded.
- Statistical outlier status can be derived or stored without modifying the raw fact.

#### Story 4: Generate Dynasty Rankings

As John, I want to generate dynasty-oriented player and pick rankings from completed trades so that I can test whether accepted trades imply useful market values.

Acceptance Criteria:

- A ranking command uses persisted completed trades, not live-only API responses.
- Recent trades have more influence than older trades.
- The first valuation model is simple enough to explain in documentation or CLI/dashboard help text.
- Ranking logic is isolated behind a boundary that can support later model improvements without rewriting crawl or persistence code.
- Players and draft picks both appear as rankable assets.
- Rankings include rank, asset name, asset type, value score, and relevant position or pick fields.
- Rankings include basic confidence/sample context.
- Ranking outputs are persisted or reproducible from persisted run inputs.

#### Story 5: Inspect Rankings in Files and CLI

As John, I want CSV and CLI outputs so that I can quickly inspect, sort, compare, and share ranking results.

Acceptance Criteria:

- The ranking command writes a CSV file with stable column names.
- The CLI prints a concise summary of crawl/ranking counts and top-ranked assets.
- Output includes the configuration context that materially affects rankings, especially season scope and run timestamp.

#### Story 6: Inspect Rankings in a Dashboard

As John, I want a lightweight rankings dashboard so that I can judge whether rankings are understandable as a future user-facing experience.

Acceptance Criteria:

- The dashboard opens to a rankings inspection table, not a marketing page or full product shell.
- The table includes rank, asset name, value score, asset type or position, and confidence/sample context.
- The dashboard supports filtering by player versus pick and by position where applicable.
- The dashboard allows selecting a player or pick to inspect recent/source trades contributing to that asset's valuation.
- The dashboard can read from local persisted ranking data.
- The dashboard remains usable on desktop and mobile viewport sizes.

#### Story 7: Compare Stability Across Runs

As John, I want to compare rankings across runs so that I can tell whether the model is credible or too noisy.

Acceptance Criteria:

- Ranking runs capture enough metadata to compare configuration and generated outputs.
- At least one validation workflow can compare ranking changes across repeated runs.
- The comparison highlights large movements or unstable assets using stored run data.

### Key Features

| Feature | Description | Priority | Notes |
|---------|-------------|----------|-------|
| Local config | Environment or ignored local config for seed username, DB path, request rate, and future lookback-window shape | Must | Keeps public repo clean |
| Sleeper client | Read-only integration with Sleeper users, leagues, transactions, picks, and players endpoints | Must | Must follow polite crawler behavior |
| Expandable crawler | Manual CLI crawl that expands through discovered users/leagues using configurable stopping limits | Must | Start broad; reduce limits if it gets unwieldy |
| Current-season scope | MVP crawls and ranks from current-season trades only | Must | Historical seasons can be revisited after the first loop is credible |
| Resumable crawler | Frontier, fetched markers, run metadata, and progress logging | Must | Scheduling is later |
| SQLite persistence | Durable local storage with clear boundary for future Postgres migration | Must | Architecture decides schema details |
| Trade fact model | Store completed trades, players, picks, league context, and raw facts | Must | Do not discard weird trades |
| Valuation engine | Generate time-weighted relative values from accepted trades | Must | Start simple, explainable, and replaceable |
| Confidence context | Display sample size, recency, league coverage, and related credibility signals | Must | Avoid false precision |
| Outlier flagging | Mark statistically unusual trades for inspection | Should | Exclusion tooling can wait |
| CSV export | Sortable rankings file | Must | First validation surface |
| CLI summary | Immediate feedback after runs | Must | Keep concise |
| Dashboard table | Thin rankings inspection UI with filters | Must | No full app shell yet |
| Source-trade drilldown | Select a ranked asset and inspect contributing trades | Should | Helps validate and debug the model |
| Optional scheduling | Local scheduled job, then free-tier cloud fallback if needed | Could | Depends on MVP reliability |
| Remote dashboard access | Inspect rankings from another device | Could | Nice-to-have only if cloud fallback makes it cheap |
| Legacy review | Review `trade-winds-legacy` for reusable lessons before architecture decisions | Should | Classify findings as reuse, discard, or rethink |

### Output Surfaces

| Surface | Purpose | Required Content | Consumer |
|---------|---------|------------------|----------|
| CLI crawl output | Immediate operator feedback during collection | Run status, progress counts, errors, and resume context | John |
| CLI ranking summary | Quick validation after ranking generation | Run timestamp, season scope, counts, and top assets | John |
| CSV export | Sortable and shareable ranking inspection | Rank, asset name, asset type, value score, position or pick fields, confidence/sample context | John |
| Dashboard rankings table | Human inspection of model output | Rank, asset name, value score, asset type/position, filters, confidence/sample context | John, future fantasy managers |
| Dashboard source-trade drilldown | Explain and debug valuations | Recent or contributing trades for a selected player or pick | John |

### Data Fidelity

- **Source facts to preserve:** Sleeper users, leagues, league settings, completed trades, trade assets, traded draft picks, player metadata snapshots, crawl frontier state, fetched markers, and crawl/ranking run metadata.
- **Derived data / recalculable outputs:** Ranking scores, rank order, confidence labels or metrics, outlier flags, source-trade contribution summaries, CSV files, and dashboard views.
- **Stable identifiers:** Sleeper user IDs, league IDs, transaction IDs, roster IDs where available, player IDs, draft-pick identifiers, crawl run IDs, and ranking run IDs.
- **Precision limits / unknowns not to invent:** Do not invent exact draft pick positions before they are known. Preserve season, round, original owner/current owner context, and exact position only when Sleeper data supports it.

---

## Non-Functional Requirements

### Performance

- Sleeper request rate must be configurable and default conservatively below 1000 calls per minute.
- Crawl progress should be visible within a few seconds of command start.
- Ranking generation should complete fast enough for interactive iteration on MVP-scale local data.
- Dashboard table should load within roughly 2 seconds for MVP-scale ranking outputs on a local machine.

### Scalability

Trade Winds should optimize for pilot and hobby scale first. The crawler should expand as far as practical through the Sleeper user-league graph while honoring configured limits for users, leagues, API calls, and runtime. MVP trade collection and rankings should use the current Sleeper season only; historical seasons and active lookback-window filtering can be added later after the crawl/model loop is credible. If broad crawling becomes unwieldy, the operator should be able to reduce limits without changing crawler logic. Persistence boundaries should keep crawler/model code from depending directly on SQLite-specific implementation details so Postgres or hosted execution can be introduced later.

### Security

- Authentication: none for MVP.
- Authorization: none for MVP local use.
- Secrets/config: seed username and operator-specific config must not be committed.
- Data handling: collect only public/read-only Sleeper API data needed for the product.
- Compliance: no formal compliance target for MVP, but API behavior must respect Sleeper documentation and avoid abusive request patterns.

### Accessibility

- Dashboard controls should be keyboard usable.
- Table content should use semantic HTML where practical.
- Color should not be the only way to communicate confidence, movement, or outlier status.
- Full WCAG certification is out of scope for MVP, but the interface should avoid obvious accessibility failures.

### Reliability

- Crawler runs must record status clearly: pending/running/completed/failed or equivalent.
- Interrupted or failed crawls must preserve completed work.
- Transient API failures should retry with backoff.
- Persistent database writes should avoid corrupting run state during partial failures.
- Local database backup is manual for MVP; automated backups belong to later deployment planning.

### Cost

- MVP should run locally with near-zero recurring cost.
- Any cloud fallback must use free-tier or very low-cost services unless John explicitly approves otherwise.
- Cloud fallback is justified if local crawls are unreliable, too slow for practical laptop use, difficult to schedule, or affected by local network/API friction.
- Remote dashboard access is not a cloud fallback trigger for MVP, but may be included if it is a low-effort side effect of the chosen fallback architecture.

---

## Acceptance Tests

### Test Case 1: Missing Config

Given no Sleeper seed username is configured, when John runs the crawl command, then the command exits with a clear error and does not create a misleading crawl run.

### Test Case 2: Successful Crawl Persistence

Given a valid Sleeper seed username and empty local database, when John runs the crawl command, then the crawler expands through discovered users and leagues until configured limits are reached, and users, leagues, current-season completed trades, crawl run metadata, and fetched markers are persisted.

### Test Case 3: Resume After Interruption

Given a crawl is interrupted after persisting partial progress, when John reruns the crawl command, then the crawler resumes from stored state and avoids refetching all previously completed work.

### Test Case 4: Trade Asset Fidelity

Given a completed trade containing players and draft picks, when the trade is persisted, then player IDs and draft-pick fields are stored without inventing unavailable exact pick positions.

### Test Case 5: Ranking Generation

Given persisted current-season completed trades, when John runs the ranking command, then Trade Winds produces ranked player and pick assets with value scores and confidence/sample context.

### Test Case 6: Recency Weighting

Given two otherwise comparable trade signals with different transaction dates, when rankings are generated, then the more recent signal has greater weight according to the configured weighting rule.

### Test Case 7: CSV and CLI Output

Given a completed ranking run, when output generation finishes, then a CSV exists with stable columns and the CLI prints a concise summary including run timestamp, season scope, counts, and top assets.

### Test Case 8: Dashboard Inspection

Given a completed ranking run, when John opens the dashboard, then a rankings table loads from local data and supports asset-type and position filtering.

### Test Case 9: Source-Trade Drilldown

Given a completed ranking run and persisted source trades, when John selects a ranked player or pick in the dashboard, then the dashboard shows recent or contributing trades used to support that asset's valuation.

### Test Case 10: Stability Comparison

Given two ranking runs with different run timestamps, when John runs the comparison workflow, then large rank/value changes are visible for inspection.

---

## Success Criteria

### Measurable Goals

- [ ] A crawl can be run, interrupted, and resumed without starting over.
- [ ] Completed trades are persisted with player and draft-pick assets.
- [ ] Rankings are generated from persisted completed trades.
- [ ] Rankings include recency weighting and confidence/sample context.
- [ ] CSV, CLI, and dashboard outputs are available for the same ranking run.
- [ ] At least one ranked asset can be traced from dashboard ranking to source trade evidence.
- [ ] John can compare ranking stability across at least two runs.
- [ ] MVP runs locally with near-zero recurring cost.

### Validation Signals

- [ ] Required outputs are inspectable by John through CLI, CSV, and dashboard surfaces.
- [ ] Rankings can be compared across repeated runs where stability matters.
- [ ] Confidence, sample size, recency, league coverage, and provenance context are visible where needed.
- [ ] Ranked assets can be traced back to source completed trades where needed.
- [ ] Current-season sample size is sufficient to judge whether historical crawling should remain deferred.

### Definition of Done

A feature is considered done when:

- [ ] Implementation matches the relevant acceptance criteria.
- [ ] Tests or validation scripts cover expected behavior and at least one failure path.
- [ ] CLI errors are understandable for the operator.
- [ ] Data changes are documented through schema/migration notes or equivalent.
- [ ] Documentation is updated when commands, config, or outputs change.
- [ ] The implementation preserves raw market facts rather than only derived values.

---

## Dependencies & Risks

### External Dependencies

| Dependency | Owner | Timeline | Risk |
|------------|-------|----------|------|
| Sleeper API | Sleeper | MVP | API availability, rate limiting, schema changes, or IP blocking |
| Sleeper player metadata | Sleeper | MVP | Metadata may be stale or incomplete |
| Local development environment | John | MVP | Local network or machine constraints may make long crawls unreliable |
| Optional free-tier cloud host | TBD | Conditional | Free-tier limits may not fit crawler behavior |
| Legacy repo reference | John | Architecture | Useful ideas may be missed or copied uncritically |

### Risks

| Risk | Mitigation | Owner |
|------|-----------|-------|
| Player and pick valuation is too noisy | Start with simple inspectable model, expose confidence context, compare stability across repeated runs | Codex + John |
| First simple model is too naive | Keep the model boundary replaceable and validate against stored facts before adding sophistication | Codex |
| Global rankings hide format differences | Store league settings in MVP and plan superflex/1QB segmentation after baseline | Codex |
| Seed graph is biased or becomes too large | Start from username seed, expand broadly, and rely on configurable limits to reduce crawl size if needed | John |
| Outlier trades distort values | Store all trades, flag statistical outliers, defer manual exclusions until needed | Codex |
| Crawler behaves impolitely or gets blocked | Configurable throttling, retries, caching, resumability, and progress logging | Codex |
| Storage choices leak into model logic | Define persistence interfaces during Architecture | Codex |
| Legacy review turns into porting by inertia | Keep review bounded and require explicit reuse/discard/rethink notes | Codex + John |
| Dashboard becomes product polish too early | Keep first dashboard to rankings inspection table and filters | Codex + John |
| Loom process becomes too heavy | Keep docs practical and move to buildable decisions quickly | Codex + John |

### Assumptions

| Assumption | Validation Plan |
|-----------|-----------------|
| Completed trades are useful market signals | Inspect ranking credibility and compare directionally against manager intuition/KTC |
| Dynasty is the right first format | Validate outputs against dynasty manager expectations before redraft work |
| Current-season trades are enough for initial validation | Inspect sample size and ranking stability before adding historical seasons or active lookback filtering |
| SQLite is sufficient for MVP | Run repeatable crawls and ranking generation locally |
| Sleeper player IDs are stable enough for identity | Store metadata snapshots and inspect unresolved/missing players |
| Confidence should be multidimensional | Display component metrics before collapsing into a single score |
| A simple explainable model is enough to validate the first loop | Compare results against manager intuition, source trades, stability, and later model candidates |
| Local-first is viable | Attempt manual and repeatable local crawls before adding cloud fallback |

### Prior Art / Legacy Inputs

| Artifact | What it shows | Keep / Discard / Rethink | Notes |
|----------|---------------|--------------------------|-------|
| `trade-winds-legacy` README | Original product idea, Sleeper crawler direction, and planned roadmap | Keep / Rethink | Preserve the accepted-trades-as-market-signal concept; re-evaluate scope through the new requirements |
| Legacy crawler | Username-seeded Sleeper graph traversal proof of concept | Keep / Rethink | Review during Architecture before final crawler design |
| Legacy in-memory storage | Early proof-of-concept storage only | Discard | MVP requires durable SQLite persistence and resumable state |
| Legacy planned API/Docker/tests | Useful future direction but not implemented | Rethink | Public API and production polish remain out of MVP |

---

## Architecture Inputs

Architecture should decide:

- Concrete language/framework choices for CLI, crawler, storage, ranking engine, and dashboard.
- Bounded review of `trade-winds-legacy`, with explicit reuse/discard/rethink notes before final stack/schema decisions.
- Whether any legacy modules or patterns should be reused intentionally.
- SQLite schema, migration approach, and repository/storage boundaries.
- Exact Sleeper API endpoint mapping and request/cache strategy.
- Crawl frontier algorithm and default stopping limits for users, leagues, API calls, and runtime.
- How to represent season scope and future lookback-window filtering so historical crawling can be added later without reshaping the whole data model.
- Ranking algorithm shape for the first valuation loop, with an explainable baseline and a replaceable model boundary.
- Dashboard delivery shape: static/local app, small server, or integrated tool.
- How the dashboard queries and displays source-trade evidence for ranked assets.
- Optional scheduling approach and minimum free-tier cloud fallback.

---

## Phase Gate

- **Ready to move to Architecture?** [x] Yes [ ] No
- **Remaining concerns:** Stack choice, exact ranking algorithm, schema design, and optional cloud fallback remain architecture decisions.
- **Owner decision:** Requirements are complete enough to proceed to Architecture after John review.

---

*Save this document in your project repo. Reference these requirements during Architecture and Implementation.*
