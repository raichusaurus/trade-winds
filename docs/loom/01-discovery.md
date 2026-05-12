# Discovery

Capture findings during the Discovery phase.

**Project Name:** trade-winds
**Date:** 2026-05-12
**Facilitator:** Codex + John Hightshue

---

## Problem Statement

### Core Problem
Trade Winds is a fantasy football market intelligence system that regularly crawls Sleeper users, leagues, and trades, then uses completed trades as weighted market signals to derive relative player valuations and rankings.

The first problem is not merely rebuilding the previous app; it is discovering what Trade Winds should be now, what the old implementation taught us, and what the smallest valuable new version should include.

### Why It Matters
A clean restart gives the project a better foundation while preserving the older repo as an artifact of prior learning. Using Loom here also gives the framework its first real pilot project.

### Current State
- The previous implementation is archived as `trade-winds-legacy`.
- The new public GitHub repository is `raichusaurus/trade-winds`.
- The new repo currently contains only this Loom documentation scaffold.
- The product direction, user, MVP, and technical architecture still need discovery.

### Legacy Implementation Snapshot
The archived implementation described Trade Winds as a modular fantasy football crawler and data engine for the Sleeper API. Its intended direction was to traverse Sleeper's user-league graph, track trades across leagues, model player value from real user behavior, and eventually expose league metadata and valuation data through an API.

Observed legacy components:

- Python command-line crawler seeded by a Sleeper username.
- Sleeper API integration for users, leagues, league users, and rosters.
- Pydantic models for Sleeper users, leagues, and rosters.
- In-memory storage for known users and leagues.
- Planned but not yet implemented persistence, API, Docker, tests, and CI.

Initial read: the old repo contains a promising domain idea and a small proof-of-concept crawler, but the new project should revalidate the product goal before choosing architecture.

The legacy implementation should be treated as reference material, not as a foundation that must be preserved. If a specific piece of the old implementation still looks good, it can be reused intentionally, but the default posture is to rebuild from scratch.

### Working Product Shape

Trade Winds has several connected responsibilities:

- Run a crawler on a regular cadence to discover Sleeper users and leagues.
- Crawl discovered users and leagues for completed trades.
- Treat each completed trade as a valid market signal.
- Weight trade signals by date, giving more recent trades more influence.
- Use weighted trade signals to infer relative player valuations and rankings.

Open product question: whether every completed trade should be treated as equally valid after date weighting, or whether future versions should account for league format, roster context, draft picks, outliers, collusion, injured players, or obvious dump trades.

### Primary User

The first useful version is optimized for John as the builder-analyst and first operator. He needs a system that can collect data, run the valuation model, inspect outputs, and decide whether the approach is credible.

The future end user is a fantasy football manager evaluating players and trades. Even if the first version is not a polished user-facing app, its output should be validated against whether it appears useful, understandable, and directionally trustworthy for that audience.

### First Useful Version

The MVP should prove the data and model before investing in a polished product surface. A lightweight dashboard is still part of MVP because it helps validate whether rankings are understandable and useful for a fantasy manager.

The first useful version should:

- Crawl Sleeper data on demand or on a repeatable cadence.
- Persist discovered users, leagues, and completed trades.
- Capture trades involving players and draft picks.
- Generate relative player and pick valuations/rankings from completed trades.
- Weight trades by recency so newer market behavior has more influence.
- Produce inspectable outputs that John can review for credibility: CSV, CLI summary, and a lightweight dashboard.

Public API polish can wait until the rankings output is useful enough to justify broader productization.

Explicitly out of scope for MVP:

- Public API.
- Account/auth system.
- Complex machine learning before the basic trade-derived model works.
- Perfect handling of every league format immediately.
- Scraping or data collection approaches that violate source terms.

MVP trade modeling should include players and draft picks. That makes the output more useful for fantasy managers, especially dynasty players, but it also means draft capital needs to be represented as a comparable asset class rather than ignored or stripped out.

The first version should optimize for dynasty fantasy football. Redraft support can be considered later, but dynasty is the natural starting point because draft picks and long-term player value are central to the market.

League format differences should be stored early, even if the first ranking output starts as a single global dynasty baseline. Superflex versus 1QB is expected to produce meaningfully different valuations, especially for quarterbacks, so format segmentation should be an explicit follow-up path rather than an afterthought.

The historical trade window should be configurable. Trade Winds should allow the operator to decide how far back to collect or include trades based on availability, model goals, and the desired balance between sample size and recency.

Crawler execution should be phased. The system should start with a manual CLI command that runs the core crawler logic, then evolve toward a scheduled local job and eventually a deployed scheduled worker. The crawl logic should be shared across these modes rather than rewritten for each runtime. While the project is local-first, MVP may still need a cloud-hosted execution path if local network conditions or API-rate issues make repeatable crawling unreliable.

Initial graph discovery should start from John's Sleeper username. This keeps the first crawl understandable and gives the operator a familiar starting point. Additional seed types, such as explicit league IDs or a stored crawl frontier, can be added later after the username-seeded path works.

The actual Sleeper username should not be committed to the public repository. It should live in environment variables or local configuration.

MVP persistence should start with SQLite because it provides real local storage and queryability without requiring external infrastructure. The storage layer should still be designed behind clear boundaries so the project can move to Postgres or another backend later without rewriting crawler and valuation logic.

The first rankings output should be a CSV file, a concise CLI summary, and a lightweight dashboard. The CSV makes rankings easy to inspect, sort, compare, and share; the CLI summary gives immediate feedback after a run; the dashboard helps validate whether the rankings make sense as a user-facing experience.

The first dashboard view should be a rankings inspection table, not a full application shell. It should stay thin and focused: rank, asset name, value score, position or asset type, sample/confidence context, and eventually recent movement. Initial filters should support player versus pick, position, and later league-format splits such as superflex versus 1QB.

Confidence should be treated as a composite signal rather than a single magical score. Useful confidence dimensions include number of trades involving the asset, number of leagues represented, recency of trade signals, stability across lookback windows, whether value is inferred directly or indirectly through connected trades, and format coverage such as whether there is enough superflex data to trust quarterback values.

For MVP, confidence can start as a simple label or set of displayed metrics, but the model should preserve enough data to support richer confidence scoring later.

Completed trades should be stored as primary market facts, even when they look strange. MVP should include all completed trades initially, while flagging statistical outliers so weird trades are visible during inspection. Manual exclusions can be added later if specific trades clearly distort model output.

Draft pick data should be stored according to what was available at the time of the trade. If a trade happened before draft order was known, the system should preserve the available season/round/team-owned pick data without inventing exact pick precision. If draft order was set and the exact pick position was known, the exact position should be stored too. Bucketing picks into early/mid/late or similar derived categories can be considered later using the stored raw data.

Player identity should be based on Sleeper player IDs, with a locally stored Sleeper player metadata snapshot for readable output. The snapshot should include enough fields for rankings and dashboard inspection, such as name, position, team, and fetch timestamp. Additional metadata sources can be considered later if Sleeper data is not enough.

Sleeper API usage should follow the official documentation and general crawler best practices. Sleeper's API is read-only and does not require an API token, but its docs advise being mindful of request frequency and staying under 1000 calls per minute to avoid IP blocking. Trade Winds should use a configurable request rate below that ceiling, retries with backoff, progress logging, response caching where useful, and resumable crawl state so failures do not force a full restart.

Resumable crawling for MVP should include persisted crawl frontier state, records of which users/leagues/trades have already been fetched, and crawl run metadata such as status, counts, errors, and timestamps. This should be implemented simply in SQLite rather than as a heavyweight orchestration system.

Ranking validation should focus on stability across runs and configurable lookback windows. Iteration is expected: early outputs may be noisy, and the model should be adjusted based on how sensitive rankings are to data window, sample size, and trade mix.

KeepTradeCut can be used as a helpful guideline, but not as ground truth. KTC represents crowdsourced opinions; Trade Winds is trying to infer value from crowdsourced facts: completed trades that managers actually accepted.

---

## Stakeholders

### Primary Stakeholders
*Who will directly benefit from solving this problem?*

| Stakeholder | Role | Needs | Constraints |
|-------------|------|-------|-------------|
| John Hightshue | Project owner / builder / first operator | A clean, useful project restart, a good Loom pilot, and valuation outputs worth trusting | Wants to preserve the old implementation as history |
| Codex | Build collaborator / Loom orchestrator | Clear context, phase outputs, and implementation boundaries | Should avoid premature scaffolding before Discovery |

### Secondary Stakeholders
*Who else is affected by this solution?*

| Stakeholder | Role | Needs | Constraints |
|-------------|------|-------|-------------|
| Fantasy football managers | Future end users / validation audience | Rankings and valuations that help evaluate players and trades | Initial version may not expose a polished product interface |
| Loom | Workflow framework under test | Feedback from real project use | Framework updates should remain separate from Trade Winds unless intentionally upstreamed |

### Decision Makers
*Who has the final say on whether we proceed?*

John Hightshue.

---

## Context & Constraints

### Timeline
- **Deadline:** No hard external deadline yet, but the project should move quickly.
- **Time to market:** High urgency because proving out Loom is part of the goal.
- **Phase-based release?** Yes. Start with a local-first MVP, but allow lightweight cloud deployment during MVP if it is needed for stable crawling. Broader automation and hosting can stay conditional on promise.

### Resources
- **Budget:** Keep costs near zero for MVP. Prefer free tiers and local-first tools unless the project shows real income potential.
- **Team:** John Hightshue and Codex.
- **Infrastructure:** Start local-first with SQLite. Use free-tier cloud services only if local execution proves unreliable or too constrained.

### Technical Constraints
- **Existing systems:** Sleeper API is the primary external system for MVP.
- **Technology requirements:** Sleeper API integration, local configuration for operator-specific secrets/settings, storage boundary that can support SQLite now and Postgres later, and flexibility to run either locally or on low-cost cloud infrastructure.
- **Scalability needs:** Pilot/hobby scale first. The first system should handle repeatable crawls and ranking generation without assuming production-scale traffic.

### Organizational Constraints
- **Compliance/Regulatory:** No known formal compliance requirements for MVP, but data collection should respect Sleeper's documented usage guidance and public API expectations.
- **Organizational policies:** Keep spending low and avoid unnecessary hosted services until there is evidence of product or income potential.
- **Dependencies:** The project depends on Loom being practical as a workflow and on Sleeper API access remaining stable enough for crawling, whether from local or low-cost cloud execution.

---

## Assumptions

### Key Assumptions
*What are you assuming to be true? What needs validation?*

| Assumption | Why We Believe It | How We'll Validate |
|-----------|------------------|-------------------|
| The rewrite should not copy the old architecture by default | The old repo is being preserved as a learning artifact, not treated as the new foundation | Review the legacy repo for lessons before architecture |
| Some legacy pieces may still be worth reusing | Starting from scratch does not require ignoring good ideas or working code | Reuse only intentionally and only if it fits the new architecture |
| Loom should begin with documentation and discovery | Loom is explicitly documentation-driven and sequential for new projects | Use this pilot to note whether that feels helpful or heavy |
| `trade-winds` should keep the canonical repo name | The legacy repo was renamed and archived | Confirm the new public repo is the active project home |
| Draft picks can be modeled alongside players | Sleeper trades often include picks, and omitting them would make many dynasty trades unusable | Start with a simple pick representation and inspect whether rankings behave plausibly |
| Dynasty is the right first fantasy format | Pick valuation and long-term player value are core to dynasty trade behavior | Validate rankings against dynasty manager expectations before considering redraft |
| League settings need to be stored before rankings are segmented | Superflex, 1QB, TE premium, scoring, and team count can materially change player value | Persist settings in MVP, then start with a global dynasty baseline and compare segmented outputs later |
| The trade history window should be configurable | Different runs may need different balances between sample size and recency | Add configuration for how far back to collect/include trades and inspect output sensitivity |
| Manual crawling should come before scheduled deployment | A CLI run is easier to debug while the data model and valuation model are still changing | Design crawler logic so manual, local scheduled, and deployed scheduled modes can share it |
| A Sleeper username is the right first crawl seed | Starting from John's username makes the first graph expansion easy to understand and verify | Implement username seeding first, then consider league ID seeds and stored frontiers |
| Seed identity belongs in local config | The repository is public, and the seed username is operator-specific | Use environment variables or ignored local config for the real Sleeper username |
| SQLite is the right MVP persistence backend | It gives real persistence and queryability without infra overhead | Keep persistence behind boundaries so Postgres can replace it later |
| CSV, CLI summary, and lightweight dashboard are enough for first output validation | The model needs inspection, and the dashboard helps judge whether output works for fantasy managers | Generate sortable CSV output, print a short run/rankings summary, and expose a simple dashboard |
| MVP may still need cloud execution | Local environments can have network or API-limit friction even when the product is still early | Keep deployment optional, but preserve a path to free-tier hosted crawling/dashboard if needed |
| A rankings table is the right first dashboard view | The first UI should help inspect valuation output, not become a full product prematurely | Build a lightweight table with rank, asset, value, type/position, confidence context, and basic filters |
| Confidence is multidimensional | No single metric captures whether a valuation is trustworthy | Track sample size, league coverage, recency, stability, directness, and format coverage where possible |
| Completed weird trades still contain market information | The core signal is accepted trades, but outliers can distort rankings | Store all completed trades, flag outliers, and consider manual exclusion later |
| Pick precision should reflect what was knowable at trade time | A future pick before draft order is set is different from an exact pick after order is known | Store raw pick data faithfully, including exact position only when available |
| Sleeper player IDs plus local metadata snapshots are enough for MVP | IDs preserve identity; metadata makes output readable | Fetch and store Sleeper player metadata with timestamped snapshots |
| Sleeper API etiquette is an explicit product constraint | The crawler depends on sustained, polite access to Sleeper's read-only API | Follow Sleeper docs, stay below their call-frequency guidance, and make request behavior configurable |
| Resumability requires both frontier and run metadata | The crawler needs to survive interruption and support repeatable runs | Persist queue/frontier state, fetched entity markers, run status, counts, errors, and timestamps |
| Ranking stability is the first credibility signal | A valuation model that swings wildly across similar runs is hard to trust | Compare outputs across runs and lookback windows before productizing |
| KeepTradeCut is a reference, not the source of truth | KTC is useful crowdsourced opinion, while Trade Winds uses completed trades as revealed behavior | Compare directionally where helpful, but do not optimize only to match KTC |

---

## Risks & Opportunities

### Risks
*What could prevent success?*

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|-----------|
| Rebuilding the old project accidentally | Medium | Medium | Mine the legacy repo for lessons, then make fresh decisions |
| Over-documenting before momentum exists | Medium | Medium | Keep phase docs practical and concise |
| Loom gaps appear during real use | Low | High | Track feedback in `pilot-feedback.md` and upstream later |
| Player and pick valuation complexity | High | Medium | Model picks explicitly, start simple, and validate outputs before adding product polish |
| Redraft assumptions leak into dynasty rankings | Medium | Low | Make dynasty the explicit first format and defer redraft-specific logic |
| Global rankings hide major league-format differences | High | High | Store format settings from the beginning; treat superflex versus 1QB as the first likely segmentation |
| Too little or too stale data produces misleading rankings | High | Medium | Make the lookback window configurable and consider labeling output confidence by data volume |
| Scheduling too early obscures crawler/model bugs | Medium | Medium | Build manual execution first, then add scheduling after behavior is observable and repeatable |
| Username seeding may create a biased initial graph | Medium | Medium | Accept this for MVP validation; expand seed strategies after the first crawler path is proven |
| Storage choices leak into business logic | High | Medium | Define persistence boundaries before implementation and avoid coupling crawler/model code directly to SQLite |
| Output format becomes product work too early | Medium | Medium | Keep the dashboard lightweight and focused on ranking inspection; defer public API, auth, and production polish |
| Local execution environment blocks reliable crawling | Medium | Medium | Keep a free-tier cloud path available for crawler or dashboard execution during MVP if necessary |
| Rankings are unstable across configuration changes | High | Medium | Treat stability across lookback windows and repeat runs as an explicit validation criterion |
| Confidence score creates false precision | Medium | Medium | Start by exposing confidence dimensions or coarse labels rather than overclaiming exact certainty |
| Outlier trades distort valuations | High | Medium | Flag statistical outliers in MVP; add manual exclusion only if inspection shows it is needed |
| Pick bucketing invents false precision or hides useful details | Medium | Medium | Store raw pick data first; derive buckets later from stored fields |
| Player metadata becomes stale | Medium | Medium | Store fetch timestamps and refresh metadata as part of repeatable runs |
| Crawler gets IP-blocked or behaves impolitely | High | Low | Use configurable throttling, retries with backoff, caching, resumability, and progress logging |
| Interrupted crawls waste work or corrupt progress | Medium | Medium | Store crawl frontier, fetched markers, and run metadata in SQLite |

### Opportunities
*What unexpected benefits might emerge?*

- Trade Winds can become both a useful project and an example Loom case study.
- The legacy implementation can reveal what to keep, discard, and rethink.
- The pilot can produce concrete improvements for Loom templates and orchestration.

---

## Discovery Outputs

### Key Insights
*What did you learn during discovery?*

- The original project was centered on fantasy football data from Sleeper, especially graph traversal and trade/player value analysis.
- The old implementation proved some basic crawling concepts but did not yet establish persistence, tests, API boundaries, or product experience.
- The old implementation should inform the rewrite, but the rewrite should not feel obligated to preserve structure unless a specific piece still earns its place.
- The new project has a clearer product center: recurring data collection from Sleeper trades, time-weighted trade signals, and relative player valuations.
- A key modeling assumption is that completed trades can be treated as valid market behavior. This is powerful because it uses real decisions instead of expert rankings, but it may need guardrails later.
- The first user is the builder-analyst, but the output must be judged by whether it would help fantasy football managers make better player and trade decisions.
- The project is intentionally fast-moving because proving out Loom is a primary objective alongside building Trade Winds.
- The first useful version should prioritize stored trade data, generated valuations/rankings, and a lightweight dashboard over API or production polish.
- MVP trade modeling includes both players and draft picks, which increases usefulness but also raises valuation complexity.
- The first target format is dynasty fantasy football; redraft can be considered after dynasty rankings are credible.
- League settings should be captured in MVP, even if the first rankings output is a global dynasty baseline. Superflex versus 1QB should be treated as an important future split.
- The historical trade lookback window should be configurable, so the operator can tune how much old market behavior feeds a ranking run.
- Crawler execution should progress from manual CLI to scheduled local job to deployed scheduled worker, with shared crawl logic underneath.
- The first crawl seed should be John's Sleeper username, with other seed types deferred until the basic graph expansion works.
- MVP persistence should use SQLite while preserving a storage boundary that allows Postgres or another backend later.
- First ranking output should include CSV, a concise CLI summary, and a lightweight dashboard.
- The first dashboard view should be a thin rankings table with basic filters and confidence/sample context.
- Confidence should account for sample size, league coverage, recency, stability, direct versus indirect inference, and format coverage.
- Store all completed trades initially, flag outliers, and defer manual exclusions until there is evidence they are needed.
- Draft picks should be stored with the information available at trade time, including exact position only when known; bucketing can be derived later.
- Player identity should use Sleeper player IDs enriched by a locally stored Sleeper metadata snapshot.
- Sleeper API access should follow official guidance and conservative crawler practices: configurable throttling, retries, caching, resumability, and progress logging.
- Resumable crawling should persist frontier state, fetched entities, and crawl run metadata in SQLite.
- Ranking credibility should be judged first by stability across runs/lookback windows, with KTC used only as a directional guideline.
- Trade Winds should distinguish crowdsourced opinion from crowdsourced facts: accepted trades are the primary signal.
- Money is the only hard technical/business constraint right now; hosted services should stay on free tiers unless the project proves income potential.
- Local-first is preferred, but MVP may still end with low-cost cloud deployment if local crawling conditions are unreliable.
- The key discovery task is to decide whether the first useful version is primarily a data engine, an analysis tool, an API product, a dashboard, or some combination staged over time.

### Open Questions
*What still needs to be explored?*

- What specific legacy patterns or modules are worth reusing, if any?
- Which concrete stack choices best fit the cost constraint while keeping iteration fast?
- What minimum cloud deployment shape is needed if local crawling proves unreliable?

### Next Steps
*What needs to happen before Requirements?*

- Summarize "keep / discard / rethink" findings from the legacy implementation.
- Turn the current Discovery answers into sharper scope boundaries for Requirements.
- Decide whether MVP planning should assume local-only execution or include a free-tier cloud fallback.
- Convert discovery answers into Requirements.

---

## Sign-Off

- **Discovery Lead:** _________________ Date: _______
- **Stakeholder:** _________________ Date: _______
- **Decision Maker:** _________________ Date: _______

**Ready to move to Requirements?** [ ] Yes [ ] No (Explain):

---

*Save this document in your project repo for future reference.*
