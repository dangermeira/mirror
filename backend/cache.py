"""A tiny in-memory cache with per-entry expiry (TTL = "time to live").

Deliberately generic and source-agnostic: it stores any value under a string key and
forgets it once ``ttl_seconds`` have passed. The clock is *injectable* so the expiry logic
is unit-testable without real waiting — the same purity trick we used for the Step-3
timestamp. ``time.monotonic`` (the default) only ever moves forward and ignores wall-clock
changes (DST, NTP), which is exactly what you want for measuring elapsed durations.
"""

import time
from collections.abc import Callable


class TTLCache:
    """Single-process, in-memory key -> value store where each entry self-expires."""

    def __init__(self, ttl_seconds: float, now: Callable[[], float] = time.monotonic):
        self._ttl = ttl_seconds
        self._now = now
        self._store: dict[str, tuple[float, object]] = {}  # key -> (expires_at, value)

    def get(self, key: str):
        """Return the cached value if present and not yet expired, else None.

        A stale entry is evicted lazily (on the read that finds it expired) rather than by
        a background sweep — simplest thing that works for the MVP.
        """
        entry = self._store.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if self._now() >= expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value) -> None:
        """Store ``value`` under ``key``, expiring ``ttl_seconds`` from now."""
        self._store[key] = (self._now() + self._ttl, value)
