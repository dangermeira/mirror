"""Unit tests for TTLCache. A hand-cranked fake clock makes expiry deterministic — we can
prove "expires after 10s" instantly, with no real waiting."""

from cache import TTLCache


class FakeClock:
    """A clock that stays put until we advance it by hand."""

    def __init__(self):
        self.t = 0.0

    def __call__(self) -> float:  # called like time.monotonic()
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds


def test_hit_before_expiry():
    clock = FakeClock()
    cache = TTLCache(ttl_seconds=10, now=clock)
    cache.set("k", "v")
    clock.advance(9)  # still within the 10s window
    assert cache.get("k") == "v"


def test_miss_after_expiry():
    clock = FakeClock()
    cache = TTLCache(ttl_seconds=10, now=clock)
    cache.set("k", "v")
    clock.advance(10)  # exactly at the TTL -> expired (get uses >=)
    assert cache.get("k") is None


def test_missing_key_returns_none():
    cache = TTLCache(ttl_seconds=10, now=FakeClock())
    assert cache.get("absent") is None
