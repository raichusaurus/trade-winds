from __future__ import annotations


def test_rate_limiter_waits_between_requests_with_fake_clock() -> None:
    from trade_winds.sleeper.rate_limit import FakeClock, RateLimiter

    clock = FakeClock(start=100.0)
    limiter = RateLimiter(requests_per_second=2.0, clock=clock)

    limiter.before_request()
    limiter.before_request()
    limiter.before_request()

    assert clock.sleep_calls == [0.5, 0.5]
    assert clock.now == 101.0


def test_rate_limiter_can_slow_down_after_stress_signal() -> None:
    from trade_winds.sleeper.rate_limit import FakeClock, RateLimiter

    clock = FakeClock(start=100.0)
    limiter = RateLimiter(requests_per_second=4.0, min_requests_per_second=0.5, clock=clock)

    limiter.slow_down(reason="rate_limit_response")
    limiter.before_request()
    limiter.before_request()

    assert limiter.effective_requests_per_second == 2.0
    assert clock.sleep_calls == [0.5]
