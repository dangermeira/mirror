"""Unit tests for the OverFast adapter's pure mapping (`_to_canonical`).

No network: we feed in captured, real-shaped OverFast responses and assert the canonical
output. Run from the backend/ directory with:  .venv/bin/python -m pytest
"""

from adapters.overfast import _to_canonical

# Trimmed but real-shaped OverFast responses (field paths per docs/architecture.md).
SAMPLE_SUMMARY = {
    "username": "TeKrop",
    "avatar": "https://example.com/avatar.png",
    "competitive": {
        "pc": {
            "tank": None,  # unranked -> should be skipped
            "damage": {"division": "diamond", "tier": 3},
            "support": {"division": "silver", "tier": 4},
            "open": None,
        },
        "console": None,
    },
}

SAMPLE_STATS = {
    "general": {"games_played": 100, "winrate": 51.45},
    "heroes": {
        "ana": {"time_played": 579942},       # 161.1h
        "zenyatta": {"time_played": 613414},  # 170.4h
        "kiriko": {"time_played": 3600},      # 1.0h
    },
}


def test_maps_core_fields():
    profile = _to_canonical("TeKrop#2217", SAMPLE_SUMMARY, SAMPLE_STATS)

    assert profile.username == "TeKrop#2217"
    assert profile.display_name == "TeKrop"
    assert profile.source == "overfast"
    assert profile.game == "overwatch2"
    assert profile.stats.win_rate == 51.45


def test_unranked_roles_are_skipped():
    profile = _to_canonical("TeKrop#2217", SAMPLE_SUMMARY, SAMPLE_STATS)
    roles = {r.role: r.rank for r in profile.stats.ranks}

    assert roles == {"damage": "Diamond 3", "support": "Silver 4"}  # tank (None) gone


def test_top_heroes_sorted_by_playtime_desc():
    profile = _to_canonical("TeKrop#2217", SAMPLE_SUMMARY, SAMPLE_STATS)
    names = [h.name for h in profile.stats.top_heroes]

    assert names == ["Zenyatta", "Ana", "Kiriko"]  # 170.4h > 161.1h > 1.0h
    assert profile.stats.top_heroes[0].playtime_hours == 170.4


def test_private_profile_is_tolerated():
    """A private profile comes back as 200 with empty stats — must not crash."""
    profile = _to_canonical("Private#1234", {"username": "Private"}, {})

    assert profile.stats.win_rate is None
    assert profile.stats.ranks == []
    assert profile.stats.top_heroes == []
