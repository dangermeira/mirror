"""Canonical failure taxonomy for Mirror.

Every adapter maps whatever a source returns into one of these fixed states, so the rest
of the app (and the frontend) deals with a small, known set of outcomes instead of raw
upstream HTTP codes. See docs/architecture.md, "Canonical error taxonomy".
"""

from enum import Enum


class SourceState(str, Enum):
    """The fixed set of failure outcomes.

    Inheriting from ``str`` makes each member behave like its string value, so it
    serializes straight to JSON (``SourceState.NOT_FOUND`` -> ``"NOT_FOUND"``).
    """

    NOT_FOUND = "NOT_FOUND"        # no such player, or a malformed username
    PRIVATE = "PRIVATE"            # profile exists but its career stats are hidden
    RATE_LIMITED = "RATE_LIMITED"  # the source is throttling us
    SOURCE_DOWN = "SOURCE_DOWN"    # the source errored, timed out, or was unreachable
    UNKNOWN = "UNKNOWN"            # anything we didn't anticipate (safety net)


# One outgoing HTTP status + friendly message per state. This table is the single source
# of truth the exception handler (in main.py) reads from.
STATE_META: dict[SourceState, tuple[int, str]] = {
    SourceState.NOT_FOUND: (404, "We couldn't find a player with that username."),
    SourceState.PRIVATE: (403, "That profile is private, so its stats can't be shown."),
    SourceState.RATE_LIMITED: (429, "We're being rate-limited by the data source. Try again shortly."),
    SourceState.SOURCE_DOWN: (503, "The stats source is unavailable right now. Try again soon."),
    SourceState.UNKNOWN: (502, "Something went wrong fetching those stats."),
}


class SourceError(Exception):
    """Raised by an adapter when a lookup fails.

    Carries the canonical ``state`` so the exception handler knows which HTTP status and
    friendly message to return — the adapter decides *what kind* of failure it is; the
    handler decides *how it looks* on the wire.
    """

    def __init__(self, state: SourceState):
        self.state = state
        super().__init__(state.value)


def classify_status(status_code: int) -> SourceState:
    """Map a raw upstream HTTP status code to a canonical failure state.

    Any 4xx means "we couldn't retrieve that player" -> NOT_FOUND (covers 404, and also a
    stricter source's 400/401/403/422); 429 is the one 4xx we treat specially; 5xx means
    the source itself failed -> SOURCE_DOWN. Anything else (e.g. an unfollowed 3xx) is
    UNKNOWN. Pure: same input always gives the same output, so it's trivial to unit-test.
    """
    if status_code == 429:
        return SourceState.RATE_LIMITED
    if 400 <= status_code < 500:
        return SourceState.NOT_FOUND
    if status_code >= 500:
        return SourceState.SOURCE_DOWN
    return SourceState.UNKNOWN
