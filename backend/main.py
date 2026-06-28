"""Mirror backend — FastAPI app entry point."""

from datetime import datetime, timezone

from fastapi import FastAPI

from models import HeroUsage, OverwatchStats, PlayerProfile, RoleRank

# `app` is the application object uvicorn runs. FastAPI auto-builds the
# interactive docs at /docs from the routes we register below.
app = FastAPI(title="Mirror API")


@app.get("/")
def root():
    """Health check: proves the server is up and responding."""
    return {"hello": "mirror"}


@app.get("/player/{username}", response_model=PlayerProfile)
def get_player(username: str):
    """Return a player's canonical profile.

    Hardcoded fake data for now (Step D) — the same stats for any username.
    The real OverFast adapter replaces this in build step 3.
    """
    return PlayerProfile(
        username=username,
        display_name=username.capitalize(),
        avatar_url="https://placehold.co/128x128",
        source="fake",
        game="overwatch2",
        last_updated=datetime.now(timezone.utc),
        stats=OverwatchStats(
            ranks=[
                RoleRank(role="tank", rank="Diamond 3"),
                RoleRank(role="damage", rank="Platinum 1"),
                RoleRank(role="support", rank="Gold 2"),
            ],
            win_rate=53.7,
            top_heroes=[
                HeroUsage(name="Reinhardt", playtime_hours=42.5),
                HeroUsage(name="Ana", playtime_hours=37.0),
                HeroUsage(name="Cassidy", playtime_hours=21.3),
            ],
        ),
    )
