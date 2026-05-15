# Trade Winds Tests

Trade Winds uses test-first development. Each service, component, class, CLI command, and
persistence contract should have failing tests before production implementation begins.

Current layout:

```text
tests/
  cli/           CLI command contracts
  contracts/     Service/interface contracts
  integration/   Multi-component behavior over temp resources
  unit/          Focused class/function behavior
  fixtures/      Handcrafted Sleeper and ranking payloads
```

Live Sleeper tests must be skipped by default and require `TRADE_WINDS_LIVE_SLEEPER=1`.
