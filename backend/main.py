"""Mirror backend — FastAPI app entry point."""

from fastapi import FastAPI

from adapters.overfast import fetch_player
from models import PlayerProfile

# `app` is the application object uvicorn runs. FastAPI auto-builds the
# interactive docs at /docs from the routes we register below.
app = FastAPI(title="Mirror API")


@app.get("/")
def root():
    """Health check: proves the server is up and responding."""
    return {"hello": "mirror"}


@app.get("/player/{username}", response_model=PlayerProfile)
async def get_player(username: str):
    """Return a player's canonical profile, fetched live from OverFast and adapted.

    `username` is a BattleTag like "Player#1234". The OverFast adapter does the HTTP
    calls and maps the response into our canonical shape; `response_model` validates and
    serializes that shape on the way out.
    """
    return await fetch_player(username)
