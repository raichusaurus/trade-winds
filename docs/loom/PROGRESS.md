# Loom Progress Ledger

Project-specific completion ledger for Trade Winds. This root file is the project cockpit. It should stand alone while the project is small, then become an index into child progress ledgers if phases, services, components, or units need their own ownership, blockers, scoring evidence, or review path.

Update this document whenever changes land on `main`, especially when:

- A phase gate opens or closes
- A workstream, service, component, or smallest tracked unit is added, removed, split, or merged
- Contracts/tests move from planned to executable, or from red to green
- Implementation scope lands
- CI/check automation changes status
- Review, acceptance, or retrospective evidence changes a score

## How Progress Is Scored

Percentages use the Loom defaults:

- `0%` = not started
- `25%` = drafted or started, major gaps remain
- `50%` = usable first pass, important gaps remain
- `75%` = mostly complete, known cleanup or validation remains
- `100%` = phase gate is satisfied for this scope
- `N/A` = phase does not apply and is excluded from calculations

Use exact percentages when there is a better signal, such as task counts, test pass counts, implementation slices, reviewed deliverables, or CI gate promotion.

Contract readiness is not the same as product readiness. A scope can be `100%` complete for Contracts & Tests while still being `0%` complete for Implementation.

Unless noted otherwise, phase weights are equal. Lower-level scopes may inherit Requirements, Architecture, and Planning credit from parent phase documents when those documents clearly define the scope, boundaries, contracts, and work ownership. Do not inherit Contracts & Tests or Implementation credit unless that lower-level scope has direct evidence.

## Recursive Progress Tree

Use one root `PROGRESS.md` first. Split child progress docs out only when a phase, service, component, or unit needs independent ownership, blockers, scoring evidence, or too much detail for the root file.

Current layout:

```text
docs/loom/
  PROGRESS.md
  phases/
    contracts-tests/PROGRESS.md
    implementation/PROGRESS.md
  scopes/
    system-design/PROGRESS.md
```

Each child progress document should include:

- Link back to its parent progress document
- Links to child progress documents when they exist
- Phase scores relevant to that zoom level
- Evidence links for each score
- Blockers, open questions, and next score-changing actions

Rule of thumb: if a scope has its own owner, contracts, implementation path, blocker surface, or review path, it can earn its own `PROGRESS.md`.

### Progress Tree Index

Child progress docs exist for the two active drilldown areas: contract readiness and implementation readiness. Add more only when a scope needs independent ownership, blockers, evidence, or review.

| Scope | Type | Parent | Total | Current Focus | Progress Doc | Notes |
|-------|------|--------|-------|---------------|--------------|-------|
| Trade Winds | Project | None | 70% | Implementation bootstrap after contract-ready Phase 5 | [Project Progress](PROGRESS.md) | Root cockpit. |
| System Design | Scope | Project | 67% | Track service/component/unit hierarchy | [System Design Progress](scopes/system-design/PROGRESS.md) | Drilldown from services to smallest tracked units. |
| Discovery | Phase | Project | 100% | Closed | [Discovery](01-discovery.md) | Child progress doc not needed. |
| Requirements | Phase | Project | 100% | Closed | [Requirements](02-requirements.md) | Child progress doc not needed. |
| Architecture | Phase | Project | 100% | Closed | [Architecture](03-architecture.md) | Child progress doc not needed. |
| Planning & Decomposition | Phase | Project | 100% | Closed | [Planning](04-planning.md) | Child progress doc not needed. |
| Contracts & Tests | Phase | Project | 100% | Contract-ready, implementation-red | [Contracts & Tests Progress](phases/contracts-tests/PROGRESS.md) | Drilldown for test coverage, gates, and deferred decisions. |
| Implementation | Phase | Project | 0% | Package scaffold next | [Implementation Progress](phases/implementation/PROGRESS.md) | Drilldown for workstreams, components, units, and next implementation actions. |
| Review & Retrospective | Phase | Project | 0% | Not started | [Retrospective](07-retrospective.md) | Child progress doc not needed yet. |
| Project Foundation | Workstream | Implementation | 67% | Create `trade_winds` scaffold | [Implementation Progress](phases/implementation/PROGRESS.md) | Implementation drilldown. |
| Persistence & Schema | Workstream | Implementation | 67% | Implement schema/repositories | [Implementation Progress](phases/implementation/PROGRESS.md) | Implementation drilldown. |
| Sleeper Client | Workstream | Implementation | 67% | Implement fake/real client boundary | [Implementation Progress](phases/implementation/PROGRESS.md) | Implementation drilldown. |
| Crawl Orchestration | Workstream | Implementation | 67% | Implement discovery/sync services | [Implementation Progress](phases/implementation/PROGRESS.md) | Implementation drilldown. |
| Transaction Normalization | Workstream | Implementation | 67% | Implement normalizer and asset keys | [Implementation Progress](phases/implementation/PROGRESS.md) | Implementation drilldown. |
| Valuation Engine | Workstream | Implementation | 67% | Implement model/confidence/outliers | [Implementation Progress](phases/implementation/PROGRESS.md) | Implementation drilldown. |
| Export & Inspection | Workstream | Implementation | 67% | Implement CSV/query/CLI surfaces | [Implementation Progress](phases/implementation/PROGRESS.md) | Implementation drilldown. |
| CI Bootstrap | Workstream | Contracts & Tests / Implementation | 75% | Promote from collection to full pytest later | [Contracts & Tests Progress](phases/contracts-tests/PROGRESS.md) | Automation/test-readiness drilldown. |

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

## Workstream Summary

| Workstream | Requirements | Architecture | Planning | Contracts & Tests | Implementation | Review | Total | Evidence |
|------------|--------------|--------------|----------|-------------------|----------------|--------|-------|----------|
| Project Foundation | 100% | 100% | 100% | 100% | 0% | 0% | 67% | [Implementation Progress](phases/implementation/PROGRESS.md) |
| Service Boundary Design | 100% | 100% | 100% | 100% | 0% | 0% | 67% | [Implementation Progress](phases/implementation/PROGRESS.md) |
| Persistence & Schema | 100% | 100% | 100% | 100% | 0% | 0% | 67% | [Implementation Progress](phases/implementation/PROGRESS.md) |
| Sleeper Client | 100% | 100% | 100% | 100% | 0% | 0% | 67% | [Implementation Progress](phases/implementation/PROGRESS.md) |
| Crawl Orchestration | 100% | 100% | 100% | 100% | 0% | 0% | 67% | [Implementation Progress](phases/implementation/PROGRESS.md) |
| Transaction Normalization | 100% | 100% | 100% | 100% | 0% | 0% | 67% | [Implementation Progress](phases/implementation/PROGRESS.md) |
| Valuation Engine | 100% | 100% | 100% | 100% | 0% | 0% | 67% | [Implementation Progress](phases/implementation/PROGRESS.md) |
| Export & Inspection | 100% | 100% | 100% | 100% | 0% | 0% | 67% | [Implementation Progress](phases/implementation/PROGRESS.md) |
| Tests & Contracts | 100% | 100% | 100% | 100% | 100% | 0% | 83% | [Contracts & Tests Progress](phases/contracts-tests/PROGRESS.md) |
| CI Bootstrap | 100% | 100% | 100% | 100% | 50% | 0% | 75% | [Contracts & Tests Progress](phases/contracts-tests/PROGRESS.md) |

## Next Score-Changing Actions

| Action | Phase / Area | Expected Score Impact | Owner |
|--------|--------------|-----------------------|-------|
| Create the minimal `trade_winds` package scaffold and keep collection green | Implementation / Project Foundation | Moves Project Foundation implementation above 0%; may increase project total if scaffold is accepted as implementation progress. | Codex |
| Implement settings/env validation and CLI help/config errors | Implementation / Project Foundation | Turns first focused red contracts green for Configuration and CLI Application units. | Codex |
| Implement `AppContext.create` dependency wiring and test override path | Implementation / Service Boundary Design | Moves App Context implementation above 0%. | Codex |
| Implement database schema creation and migration helpers | Implementation / Persistence & Schema | Moves schema/migration units above 0% and unlocks repository work. | Codex |
| Promote CI from `pytest --collect-only` to focused/full pytest when green enough | CI Bootstrap | Moves CI Bootstrap implementation beyond 50%. | Codex |
| Choose Pyright or mypy | CI Bootstrap / Type checking | Allows type-check automation scoring to move from deferred to planned or implemented. | John + Codex |

## Decisions and Adjustments

| Date | Scope | Change | Reason | Owner |
|------|-------|--------|--------|-------|
| 2026-05-18 | Project | Added recursive progress ledger | Loom framework now expects percent complete by project, workstream, component, and smallest tracked unit. | Codex |
| 2026-05-18 | Contracts & Tests | Counted Phase 5 as 100% contract-ready | Missing CLI command contracts were added and remaining needs are implementation-facing. | Codex |
| 2026-05-18 | CI Bootstrap | Counted CI as 50% implemented inside its workstream | Collection/Ruff workflow exists; full pytest, coverage, type checking, and migration gates are deferred until implementation can pass them. | Codex |
| 2026-05-18 | Progress ledger organization | Added root cockpit rules, update triggers, progress tree index, and next score-changing actions | Loom framework refined how progress ledgers should organize recursive drilldowns. | Codex |

## Open Progress Questions

| Scope | Question | Needed To Score Accurately | Owner |
|-------|----------|----------------------------|-------|
| Type checking | Pyright or mypy? | Decide before scoring type-check automation beyond deferred. | John + Codex |
| HTTP mocking | `pytest-httpx` or `respx`? | Decide during Sleeper client implementation if fixture transport is not enough. | Codex |
| Scope weights | Should MVP delivery weight persistence/crawl/valuation more heavily than docs/governance? | Current rollup uses equal weights; adjust if delivery progress should dominate. | John |
| CI/CD phase shape | Should CI/CD become a standalone Loom phase/checkpoint? | Current project treats it as a bootstrap workstream; framework question remains open. | John |
