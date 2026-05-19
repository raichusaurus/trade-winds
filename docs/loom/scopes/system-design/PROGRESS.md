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
| Project Foundation | 1 | 67% | 67% | 67% | [Project Foundation Progress](../services/project-foundation/PROGRESS.md) | Config, CLI shell, package scaffold. |
| Service Boundary Design | 1 | 67% | 67% | 67% | [Service Boundary Progress](../services/service-boundary-design/PROGRESS.md) | App context and application services. |
| Persistence & Schema | 1 | 67% | 67% | 67% | [Persistence Progress](../services/persistence-schema/PROGRESS.md) | SQLite schema, migrations, repositories. |
| Sleeper Client | 1 | 67% | 67% | 67% | [Sleeper Client Progress](../services/sleeper-client/PROGRESS.md) | API client, resilience, test doubles. |
| Crawl Orchestration | 1 | 67% | 67% | 67% | [Crawl Progress](../services/crawl-orchestration/PROGRESS.md) | Discovery and transaction sync. |
| Transaction Normalization | 1 | 67% | 67% | 67% | [Normalization Progress](../services/transaction-normalization/PROGRESS.md) | Asset identity, trade/add-drop normalization. |
| Valuation Engine | 1 | 67% | 67% | 67% | [Valuation Progress](../services/valuation-engine/PROGRESS.md) | Model, confidence, outliers, ranking generation. |
| Export & Inspection | 1 | 67% | 67% | 67% | [Export & Inspection Progress](../services/export-inspection/PROGRESS.md) | CSV export and query/CLI inspection. |
| **Child Rollup** | | | | **67%** | | Equal-weight average. |

## Next Score-Changing Actions

| Action | Phase / Area | Expected Score Impact | Owner |
|--------|--------------|-----------------------|-------|
| Create `trade_winds` package scaffold | Implementation / system design | Moves implementation above 0% for foundation units. | Codex |
| Split a component into its own child progress doc | Progress organization | Improves navigation if a component develops independent blockers or ownership. | Codex |

## Blockers and Questions

| Item | Impact | Owner | Next Step |
|------|--------|-------|-----------|
| Production modules not created | All system-design units remain 0% implementation. | Codex | Start implementation bootstrap. |
| Scope weights are equal by default | May understate/overstate heavy persistence/crawl/valuation work. | John | Decide whether to weight services by effort or risk later. |
