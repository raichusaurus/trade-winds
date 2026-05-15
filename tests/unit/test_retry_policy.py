from __future__ import annotations

import pytest


def test_retry_policy_retries_transient_errors_with_bounded_attempts() -> None:
    from trade_winds.sleeper.retry import RetryPolicy, TransientSleeperError

    attempts = []

    def flaky_call() -> str:
        attempts.append("attempt")
        if len(attempts) < 3:
            raise TransientSleeperError("temporary")
        return "ok"

    policy = RetryPolicy(max_attempts=3, base_delay_seconds=0)

    assert policy.run(flaky_call) == "ok"
    assert len(attempts) == 3


def test_retry_policy_does_not_retry_permanent_errors() -> None:
    from trade_winds.sleeper.retry import PermanentSleeperError, RetryPolicy

    attempts = []

    def failing_call() -> str:
        attempts.append("attempt")
        raise PermanentSleeperError("not found")

    policy = RetryPolicy(max_attempts=3, base_delay_seconds=0)

    with pytest.raises(PermanentSleeperError):
        policy.run(failing_call)

    assert attempts == ["attempt"]


def test_retry_policy_raises_last_transient_error_after_attempts_exhausted() -> None:
    from trade_winds.sleeper.retry import RetryAttemptsExhausted, RetryPolicy, TransientSleeperError

    def always_failing_call() -> str:
        raise TransientSleeperError("still failing")

    policy = RetryPolicy(max_attempts=2, base_delay_seconds=0)

    with pytest.raises(RetryAttemptsExhausted, match="2 attempts"):
        policy.run(always_failing_call)
