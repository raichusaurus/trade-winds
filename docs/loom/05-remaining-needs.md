# Phase 5 Remaining Needs

This file is the handoff from Contracts & Tests / CI/CD into implementation. Phase 5 has enough executable contracts to begin implementation; the items below are intentionally not additional contract-writing blockers.

## Contract Status

- Schema, repository, Sleeper client, rate limiting, retry, normalization, valuation, confidence, outlier, export, inspection, fixture workflow, and live-smoke contracts are represented by tests.
- CLI contracts now cover help/config errors, crawl discovery options, crawl transaction sync dispatch, ranking generation options, export rankings, inspection filters, asset evidence, and run comparison.
- CI contract readiness exists in `.github/workflows/ci.yml` with local command parity and live tests skipped by default.

## Remaining Before Green Implementation

- Create the `trade_winds` package scaffold and wire imports used by the existing tests.
- Implement settings loading, app context dependency wiring, and test override hooks.
- Implement the SQLite schema/migration helpers and repository bundle.
- Implement Sleeper client transports, retry/rate-limit helpers, fixture-backed fake clients, and controlled errors.
- Implement transaction normalization for trades, picks, add/drop movement, warnings, and raw-payload preservation.
- Implement ranking generation, confidence/outlier calculations, ranking persistence, query, export, and comparison services.
- Implement CLI command bodies so they call application services and print stable summaries.
- Decide on Pyright or mypy before adding type checking to CI.
- Update `docs/loom/PROGRESS.md` with each main-branch push, especially as red contracts turn green and implementation units are added.

## Verification Commands

Use the repository-local uv cache when running inside the Codex sandbox:

```bash
env UV_CACHE_DIR=.uv-cache uv run pytest
env UV_CACHE_DIR=.uv-cache uv run ruff check .
env UV_CACHE_DIR=.uv-cache uv run ruff format --check .
```

Expected current state before implementation: pytest collects the suite, the live Sleeper smoke test is skipped by default, and the executable contracts fail until `trade_winds` exists.
