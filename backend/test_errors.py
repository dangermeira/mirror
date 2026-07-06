"""Unit tests for the canonical failure taxonomy (errors.py). All pure — no network."""

from errors import STATE_META, SourceError, SourceState, classify_status


def test_classify_known_statuses():
    assert classify_status(404) == SourceState.NOT_FOUND
    assert classify_status(422) == SourceState.NOT_FOUND  # any 4xx -> couldn't fetch player
    assert classify_status(403) == SourceState.NOT_FOUND
    assert classify_status(429) == SourceState.RATE_LIMITED  # the one special-cased 4xx
    assert classify_status(500) == SourceState.SOURCE_DOWN
    assert classify_status(503) == SourceState.SOURCE_DOWN


def test_classify_unexpected_status_is_unknown():
    assert classify_status(302) == SourceState.UNKNOWN  # e.g. an unfollowed 3xx redirect


def test_every_state_has_metadata():
    """Guards against adding a new state but forgetting its status + message."""
    for state in SourceState:
        assert state in STATE_META
        status, message = STATE_META[state]
        assert 400 <= status < 600
        assert message  # non-empty


def test_source_error_carries_state():
    err = SourceError(SourceState.PRIVATE)
    assert err.state == SourceState.PRIVATE
