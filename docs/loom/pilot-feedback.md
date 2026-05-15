# Loom Pilot Feedback

Use this file to capture observations about using Loom on Trade Winds.

## What Works

- The phase sequence gives the rewrite a clear starting point before implementation.
- Keeping the legacy repo separate makes it easier to learn from the old project without copying it by default.

## Friction

- The earlier phases identified the right components and sequencing, but they did not force enough **contract precision** before the Contracts & Tests phase. In practice, Phase 5 had to discover and backfill missing details that should have been prompted earlier.
- The database schema was initially described as a data model, but not as a **schema contract** with primary keys, uniqueness/idempotency constraints, nullable fields, foreign-key intent, and required raw JSON columns.
- Planning named "CI/CD" as part of Phase 5, but the workflow did not clearly distinguish between:
  - documenting CI/CD intent,
  - creating the CI workflow,
  - deciding when CI becomes blocking,
  - and deferring CI while tests are intentionally red.
- The testing template asked for test strategy, but did not explicitly ask for a **gap register** that separates:
  - covered by executable tests,
  - intentionally deferred,
  - blocked by tooling,
  - and future/live/manual checks.
- The phase gate from Planning to Contracts & Tests allowed implementation to seem close even though schema, repository, endpoint, valuation, and CI contracts were not fully locked.
- It was easy to write high-level acceptance tests before all lower-level contracts existed. That is useful, but Loom should prompt for a layered test inventory so foundational contracts are not accidentally skipped.
- There was no explicit prompt to decide whether test directories should mirror production modules or group by test category. This is worth making intentional because pre-implementation TDD often benefits from category grouping, while mature repos often prefer mirrored layout.
- The CI/CD section did not ask for a dependency lockfile policy, local/CI command parity, live-test policy, secrets policy, or required-check promotion path.
- The templates did not ask for type-checking policy early enough. Choosing "defer Pyright/mypy until scaffold" is fine, but the decision should be visible as a tracked gap.
- There was no explicit "red-test policy" for TDD: when intentional failing tests are acceptable, when they should be isolated, and when CI should start enforcing green status.

## Framework Improvements To Consider

- Add a **Contract Completeness Checkpoint** before Implementation. This should require project-specific answers for:
  - schema/table contracts,
  - service/API contracts,
  - repository method contracts,
  - CLI command/option contracts,
  - external integration contracts,
  - model/algorithm invariants,
  - fixture inventory,
  - CI bootstrap plan.
- Update the Architecture template to include a "Schema Contract" section when persistence is in scope. Suggested prompts:
  - What are the required tables/entities?
  - What are the primary keys?
  - What uniqueness constraints make ingestion idempotent?
  - Which fields are nullable and why?
  - Which raw payload/source fields must be preserved?
  - Which foreign keys should exist now versus later?
  - Which fields are required for future inspection/debugging?
- Update the Planning template to include a separate **CI Bootstrap** slice when CI/CD is in scope. It should have explicit dependencies such as package scaffold, lockfile, test runner, and first green implementation slice.
- Update the Contracts & Tests template to include a **Testing Gap Register** with statuses:
  - Covered by executable test.
  - Planned before slice implementation.
  - Deferred until tooling exists.
  - Manual/opt-in only.
  - Out of scope.
- Add prompts for **test layering**:
  - Unit tests for pure behavior.
  - Contract tests for service/repository/client boundaries.
  - Integration tests for persistence and multi-component workflows.
  - CLI tests for operator behavior.
  - End-to-end fixture workflow tests.
  - Live smoke tests that are opt-in and non-blocking.
- Add a **red-test policy** prompt:
  - Are intentionally failing tests allowed on the branch?
  - How are red tests marked or communicated?
  - When should CI become blocking?
  - What is the first required green checkpoint?
- Add CI/CD prompts:
  - What command installs dependencies locally and in CI?
  - Is there a lockfile?
  - Which checks are blocking now?
  - Which checks become blocking later?
  - Which checks are informational?
  - Which tests require secrets or network access?
  - Are live tests manual, scheduled, or PR-gated?
- Add a **fixture inventory** prompt for projects with external integrations:
  - Happy-path payloads.
  - Empty responses.
  - Malformed/partial responses.
  - Not-found responses.
  - Retryable/transient failures.
  - Edge cases discovered from real data.
- Add a **repository contract prompt** when persistence exists:
  - What methods must exist?
  - What does each method return?
  - Which methods are idempotent?
  - How are duplicate facts detected?
  - How are state transitions represented?
- Add an **algorithm/model contract prompt** when scoring/ranking/ML/business rules exist:
  - What are deterministic fixture inputs?
  - What exact outputs are expected?
  - What invariants must always hold?
  - What confidence/uncertainty fields must be exposed?
  - What edge cases must be preserved rather than discarded?
- Add a prompt to decide **test directory structure**:
  - Mirror production code.
  - Group by test type.
  - Hybrid.
  - Why this shape fits the current project phase.
- Add a prompt to decide **type-checking policy**:
  - Pyright, mypy, or deferred.
  - When it becomes CI-enforced.
  - Known integration concerns such as SQLAlchemy typing.

## Questions For Loom

- How much project-specific initialization should happen before Discovery?
- Should Loom provide a standard repo scaffold for phase documents?
- Should CI/CD be part of Phase 5, or should it become its own explicit phase/checkpoint between Contracts & Tests and Implementation?
- Should Loom support a "contract lock" phase gate that prevents Implementation until schema/service/repository/CLI/external-integration contracts are all either covered or intentionally deferred?
- Should the framework distinguish between "tests are written" and "tests are green" when TDD intentionally writes red tests before implementation?
- Should Loom templates include a standard "Known Gaps / Deferred Checks" table in every phase gate?
- Should persistence-heavy projects be required to produce an executable schema contract before implementation?
- Should external-API projects be required to produce a fixture inventory before implementation?
- Should live tests be treated as a standard non-blocking test category in Loom?
- Should the Implementation phase start with "make test tooling runnable" before feature implementation?

## Reusable Template Checklist Draft

Use this checklist to improve future Loom templates.

### Architecture

- [ ] Component boundaries include inputs, outputs, owners, and "must not do" constraints.
- [ ] Persistence projects include schema contract details, not only data-model prose.
- [ ] External integrations list endpoint methods, raw payload preservation, retry/error behavior, and fixture needs.
- [ ] CLI/API surfaces list initial command/route names and option/parameter contracts.
- [ ] Algorithms/models list deterministic inputs, expected outputs, invariants, and uncertainty fields.
- [ ] Dependency rules are explicit enough to write architecture tests or review checks.

### Planning

- [ ] Implementation slices include contract-lock work before implementation work.
- [ ] Schema contract lock is a slice when persistence exists.
- [ ] CI bootstrap is a slice when CI/CD is in scope.
- [ ] Checkpoints include required evidence, not just completion labels.
- [ ] Phase gate lists unresolved contract gaps.
- [ ] Phase gate says which gaps block implementation and which are intentionally deferred.

### Contracts & Tests / CI/CD

- [ ] Test framework and directory structure are intentionally chosen.
- [ ] Test categories are mapped to project risks.
- [ ] Every service/component/class has a test target.
- [ ] Schema, repository, endpoint, CLI, and model contracts are executable or explicitly deferred.
- [ ] Fixture inventory exists for external data.
- [ ] Known testing gaps are tracked by status.
- [ ] Red-test policy is documented.
- [ ] CI current status is documented.
- [ ] CI bootstrap plan exists with local/CI command parity.
- [ ] Live/network tests are opt-in by default.
- [ ] Coverage/type-check/migration checks have a promotion path.
