"""OverFast adapter — fetch an Overwatch 2 profile and map it to Mirror's canonical shape.

Two responsibilities, deliberately kept apart:
- `fetch_player()` does the I/O. It's ``async`` because its whole job is awaiting two
  HTTP calls to the OverFast API — while it waits, the server is free to do other work.
- `_to_canonical()` is pure mapping: dicts in, a `PlayerProfile` out, no network. That
  purity is what makes it trivial to unit-test (see test_overfast.py).
"""

import asyncio
import logging
from datetime import datetime, timezone

import httpx

from errors import SourceError, SourceState, classify_status
from models import HeroUsage, OverwatchStats, PlayerProfile, RoleRank

logger = logging.getLogger(__name__)

BASE_URL = "https://overfast-api.tekrop.fr"
ROLES = ("tank", "damage", "support")
TOP_HEROES_COUNT = 5
PLACEHOLDER_AVATAR = "https://placehold.co/128x128"


def to_player_id(username: str) -> str:
    """BattleTag → OverFast player id: the "#" becomes a "-". The single home
    for this transform — the route's cache key builds on it too."""
    return username.replace("#", "-")


async def fetch_player(username: str) -> PlayerProfile:
    """Fetch a player's OW2 profile from OverFast and return our canonical shape.

    `username` is a BattleTag like "Player#1234"; OverFast wants the "#" as a "-".
    """
    player_id = to_player_id(username)
    # One line per upstream trip: this is how cache behavior stays observable.
    logger.info("fetching %s from OverFast", player_id)
    try:
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
            # Both calls are independent, so fire them concurrently and wait for both:
            # asyncio.gather starts them at once → total wait ≈ the slower one, not the sum.
            summary_resp, stats_resp = await asyncio.gather(
                client.get(f"/players/{player_id}/summary"),
                client.get(f"/players/{player_id}/stats/summary"),
            )
    except httpx.RequestError as exc:
        # Connection refused, DNS failure, or timeout — the source is effectively down.
        raise SourceError(SourceState.SOURCE_DOWN) from exc

    # BOTH calls must return 200. Map any non-200 to a canonical failure state instead of
    # faking an empty-but-"successful" profile (classify_status turns e.g. 404 -> NOT_FOUND).
    for resp in (summary_resp, stats_resp):
        if resp.status_code != 200:
            raise SourceError(classify_status(resp.status_code))

    try:
        summary = summary_resp.json()
        stats = stats_resp.json()
    except ValueError as exc:
        # A 200 whose body isn't valid JSON (e.g. an HTML error/maintenance page from a
        # proxy) means the source misbehaved — treat it as down rather than crashing.
        raise SourceError(SourceState.SOURCE_DOWN) from exc

    # A private career returns 200 with an empty stats body — surface it as its own state
    # rather than a valid-but-empty profile. (Heuristic; see docs/decisions.md.)
    if is_private(stats):
        raise SourceError(SourceState.PRIVATE)

    # Read the clock here (the I/O "edge"), then hand it to the pure mapping.
    fetched_at = datetime.now(timezone.utc)
    return _to_canonical(username, summary, stats, fetched_at)


def is_private(stats: dict) -> bool:
    """True when a 200 response carries no usable stats — OverFast's signal for a private
    career. Pure, so it's unit-testable. Heuristic: indistinguishable from a brand-new
    public account with zero recorded stats (documented in docs/decisions.md).
    """
    return not stats.get("general") and not stats.get("heroes")


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
