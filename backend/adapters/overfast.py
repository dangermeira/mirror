"""OverFast adapter — fetch an Overwatch 2 profile and map it to Mirror's canonical shape.

Two responsibilities, deliberately kept apart:
- `fetch_player()` does the I/O. It's ``async`` because its whole job is awaiting two
  HTTP calls to the OverFast API — while it waits, the server is free to do other work.
- `_to_canonical()` is pure mapping: dicts in, a `PlayerProfile` out, no network. That
  purity is what makes it trivial to unit-test (see test_overfast.py).
"""

from datetime import datetime, timezone

import httpx
from fastapi import HTTPException

from models import HeroUsage, OverwatchStats, PlayerProfile, RoleRank

BASE_URL = "https://overfast-api.tekrop.fr"
ROLES = ("tank", "damage", "support")
TOP_HEROES_COUNT = 5
PLACEHOLDER_AVATAR = "https://placehold.co/128x128"


async def fetch_player(username: str) -> PlayerProfile:
    """Fetch a player's OW2 profile from OverFast and return our canonical shape.

    `username` is a BattleTag like "Player#1234"; OverFast wants the "#" as a "-".
    """
    player_id = username.replace("#", "-")
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        summary_resp = await client.get(f"/players/{player_id}/summary")
        stats_resp = await client.get(f"/players/{player_id}/stats/summary")

    # Minimal guard for now. Step 4 replaces this with the canonical error taxonomy
    # (NOT_FOUND / PRIVATE / RATE_LIMITED / SOURCE_DOWN) mapped to friendly states.
    if summary_resp.status_code != 200:
        raise HTTPException(
            status_code=summary_resp.status_code,
            detail=f"OverFast returned {summary_resp.status_code} for '{username}'.",
        )

    summary = summary_resp.json()
    # A private profile still returns 200 on /summary but empty stats — tolerate that.
    stats = stats_resp.json() if stats_resp.status_code == 200 else {}
    return _to_canonical(username, summary, stats)


def _to_canonical(username: str, summary: dict, stats: dict) -> PlayerProfile:
    """Pure mapping: OverFast's JSON -> our canonical PlayerProfile. No network here."""
    general = stats.get("general") or {}
    return PlayerProfile(
        username=username,
        display_name=summary.get("username") or username,
        avatar_url=summary.get("avatar") or PLACEHOLDER_AVATAR,
        source="overfast",
        game="overwatch2",
        last_updated=datetime.now(timezone.utc),
        stats=OverwatchStats(
            ranks=_extract_ranks(summary),
            win_rate=general.get("winrate"),
            top_heroes=_extract_top_heroes(stats),
        ),
    )


def _extract_ranks(summary: dict) -> list[RoleRank]:
    """PC competitive rank per role, formatted like "Diamond 3"; skip unranked roles."""
    pc = (summary.get("competitive") or {}).get("pc") or {}
    ranks: list[RoleRank] = []
    for role in ROLES:
        entry = pc.get(role)  # None when the role is unranked
        if entry and entry.get("division") and entry.get("tier") is not None:
            label = f"{entry['division'].capitalize()} {entry['tier']}"
            ranks.append(RoleRank(role=role, rank=label))
    return ranks


def _extract_top_heroes(stats: dict) -> list[HeroUsage]:
    """Top heroes by time played (OverFast gives seconds -> we want hours), highest first."""
    heroes = stats.get("heroes") or {}
    by_playtime = sorted(
        heroes.items(),
        key=lambda kv: kv[1].get("time_played", 0),
        reverse=True,
    )
    return [
        HeroUsage(
            name=_hero_name(slug),
            playtime_hours=round((data.get("time_played") or 0) / 3600, 1),
        )
        for slug, data in by_playtime[:TOP_HEROES_COUNT]
    ]


def _hero_name(slug: str) -> str:
    """OverFast hero slug -> display name, e.g. "soldier-76" -> "Soldier 76".

    Good enough for the MVP. A few names aren't perfect (e.g. "dva" -> "Dva"); we can map
    slugs to exact names via OverFast's /heroes endpoint later if we want them precise.
    """
    return slug.replace("-", " ").title()
