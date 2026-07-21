"""Route-level tests for main.py."""

import asyncio
from collections import defaultdict

import main
from cache import TTLCache


def test_concurrent_cold_misses_fetch_upstream_once(monkeypatch):
    """Two simultaneous requests for the same cold key must produce ONE
    upstream fetch (per-key lock + re-check), not a stampede of two."""
    calls = 0

    async def fake_fetch(username):
        nonlocal calls
        calls += 1
        # Yield the event loop mid-"fetch" so the second request truly
        # overlaps the first — without this, the test passes even unlocked.
        await asyncio.sleep(0)
        return {"fake": "profile"}

    monkeypatch.setattr(main, "fetch_player", fake_fetch)
    monkeypatch.setattr(main, "player_cache", TTLCache(ttl_seconds=main.CACHE_TTL_SECONDS))
    # Fresh locks too: an asyncio.Lock binds to the event loop that first
    # contends it, so reusing the module-global map across asyncio.run() calls
    # would poison later same-key tests with a lock bound to a dead loop.
    monkeypatch.setattr(main, "_key_locks", defaultdict(asyncio.Lock))

    async def run_pair():
        return await asyncio.gather(
            main.get_player("TeKrop#2217"),
            main.get_player("TeKrop#2217"),
        )

    first, second = asyncio.run(run_pair())

    assert calls == 1
    assert first is second  # the second request was served the stored copy
