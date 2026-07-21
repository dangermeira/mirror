"""Mirror backend — FastAPI app entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from adapters.overfast import fetch_player
from cache import TTLCache
from errors import STATE_META, SourceError
from models import PlayerProfile

# `app` is the application object uvicorn runs. FastAPI auto-builds the
# interactive docs at /docs from the routes we register below.
app = FastAPI(title="Mirror API")

# The browser releases our responses to a cross-origin page only if we name the
# page's origin here. Dev frontend origins only; the API serves nothing but GET.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET"],
)

# One process-wide cache so repeat searches skip OverFast. Keys are namespaced by
# game + source (per architecture.md) so a second game can't collide with OW2 entries.
CACHE_TTL_SECONDS = 300  # 5 minutes — career stats don't change second-to-second
player_cache = TTLCache(ttl_seconds=CACHE_TTL_SECONDS)


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
    cache_key = f"overwatch2:overfast:{username.replace('#', '-')}"
    cached = player_cache.get(cache_key)
    if cached is not None:
        return cached

    profile = await fetch_player(username)
    player_cache.set(cache_key, profile)
    return profile
