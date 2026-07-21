"""Mirror backend — FastAPI app entry point."""

import asyncio
import logging
import os
from collections import defaultdict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from adapters.overfast import fetch_player, to_player_id
from cache import TTLCache
from errors import STATE_META, SourceError
from models import PlayerProfile

# `app` is the application object uvicorn runs. FastAPI auto-builds the
# interactive docs at /docs from the routes we register below.
# Give log lines a handler, but keep third-party INFO chatter (httpx logs two
# lines per request) off: root stays at WARNING, only our adapter speaks INFO.
logging.basicConfig(level=logging.WARNING)
logging.getLogger("adapters").setLevel(logging.INFO)

app = FastAPI(title="Mirror API")

# The browser releases our responses to a cross-origin page only if we name the
# page's origin here. Comma-separated env override per the config invariant
# (see backend/.env.example); defaults cover the dev frontend. GET only.
ALLOWED_ORIGINS = os.environ.get(
    "MIRROR_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET"],
)

# One process-wide cache so repeat searches skip OverFast. Keys are namespaced by
# game + source (per architecture.md) so a second game can't collide with OW2 entries.
CACHE_TTL_SECONDS = 300  # 5 minutes — career stats don't change second-to-second
player_cache = TTLCache(ttl_seconds=CACHE_TTL_SECONDS)

# One lock per cache key: simultaneous cold misses for the same player queue here
# so only the first does the OverFast trip (stampede fix — see docs/decisions.md).
# Grows one entry per key ever searched, failures included, and never shrinks;
# the bounded version (in-flight future map) is a recorded deferral.
_key_locks: defaultdict[str, asyncio.Lock] = defaultdict(asyncio.Lock)


@app.exception_handler(SourceError)
async def handle_source_error(request, exc: SourceError):
    """Render a canonical failure state as an HTTP response the frontend can branch on:
    the state's mapped status code + a small JSON body {state, message}."""
    status, message = STATE_META[exc.state]
    return JSONResponse(
        status_code=status,
        content={"state": exc.state.value, "message": message},
    )


@app.get("/")
def root():
    """Health check: proves the server is up and responding."""
    return {"hello": "mirror"}


@app.get("/player/{username}", response_model=PlayerProfile)
async def get_player(username: str):
    """Return a player's canonical profile, fetched live from OverFast and adapted.

    `username` is a BattleTag like "Player#1234". We check the TTL cache first; on a miss
    we fetch via the adapter and cache the result. Only *successful* lookups are cached —
    a failure raises inside `fetch_player`, before we reach `set`. `response_model`
    validates and serializes the canonical shape on the way out.
    """
    cache_key = f"overwatch2:overfast:{to_player_id(username)}"
    cached = player_cache.get(cache_key)
    if cached is not None:
        return cached

    async with _key_locks[cache_key]:
        # Re-check: while we waited for the lock, the request ahead of us may
        # have fetched and stored this exact profile.
        cached = player_cache.get(cache_key)
        if cached is not None:
            return cached

        profile = await fetch_player(username)
        player_cache.set(cache_key, profile)
        return profile
