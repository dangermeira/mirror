"""OverFast adapter — fetch an Overwatch 2 profile and map it to Mirror's canonical shape.

Two responsibilities, deliberately kept apart:
- `fetch_player()` does the I/O. It's ``async`` because its whole job is awaiting two
  HTTP calls to the OverFast API — while it waits, the server is free to do other work.
- `_to_canonical()` is pure mapping: dicts in, a `PlayerProfile` out, no network. That
  purity is what makes it trivial to unit-test (see test_overfast.py).
"""

import asyncio
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
        # Both calls are independent, so fire them concurrently and wait for both:
        # asyncio.gather starts them at once → total wait ≈ the slower one, not the sum.
        summary_resp, stats_resp = await asyncio.gather(
            client.get(f"/players/{player_id}/summary"),
            client.get(f"/players/{player_id}/stats/summary"),
        )

    # Minimal guard for now: BOTH calls must return 200. A genuinely private profile
    # still returns 200 with an empty stats body (handled fine below); a non-200 is a
    # real error (rate-limited, source-down), so we raise rather than fake an
    # empty-but-"successful" profile. Step 4 maps these to friendly states
    # (NOT_FOUND / PRIVATE / RATE_LIMITED / SOURCE_DOWN).
    for resp in (summary_resp, stats_resp):
        if resp.status_code != 200:
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"OverFast returned {resp.status_code} for '{username}'.",
            )

    # Read the clock here (the I/O "edge"), then hand it to the pure mapping.
    fetched_at = datetime.now(timezone.utc)
    return _to_canonical(username, summary_resp.json(), stats_resp.json(), fetched_at)


def _to_canonical(
    username: str, summary: dict, stats: dict, last_updated: datetime
) -> PlayerProfile:
    """Pure mapping: inputs in, a PlayerProfile out — no network and no clock read, so
    the same inputs always produce the same output (fully unit-testable)."""
    general = stats.get("general") or {}
    return PlayerProfile(
        username=username,
        display_name=summary.get("username") or username,
        avatar_url=summary.get("avatar") or PLACEHOLDER_AVATAR,
        source="overfast",
        game="overwatch2",
        last_updated=last_updated,
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
        key=lambda kv: kv[1].get("time_played") or 0,
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
