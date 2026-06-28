"""Canonical data shapes for Mirror, defined as Pydantic models.

These models ARE the canonical shape from docs/architecture.md: every adapter
must produce a PlayerProfile, and the frontend only ever consumes this. The
universal fields live on PlayerProfile; game-specific fields live in a nested
stats model (OverwatchStats for now), so adding a second game doesn't reshape
the core.
"""

from datetime import datetime

from pydantic import BaseModel


# --- Game-shaped (Overwatch 2) -------------------------------------------

class RoleRank(BaseModel):
    """A player's rank in one OW2 role."""

    role: str  # "tank", "damage", or "support"
    rank: str  # human-readable, e.g. "Diamond 3"


class HeroUsage(BaseModel):
    """How much a player has played a given hero."""

    name: str
    playtime_hours: float


class OverwatchStats(BaseModel):
    """The OW2-specific portion of a profile."""

    ranks: list[RoleRank]
    win_rate: float  # percentage, 0-100
    top_heroes: list[HeroUsage]


# --- Universal core -------------------------------------------------------

class PlayerProfile(BaseModel):
    """The canonical profile the frontend consumes, regardless of source/game."""

    username: str
    display_name: str
    avatar_url: str
    source: str  # which data source produced this, e.g. "overfast"
    game: str  # e.g. "overwatch2"
    last_updated: datetime
    stats: OverwatchStats  # game-shaped; becomes a union when game #2 lands
