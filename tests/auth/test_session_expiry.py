"""Tests for inactivity expiry. Protects session-auth Requirement 1."""

from datetime import timedelta

from src.auth.session import SessionManager


def test_active_session_is_valid():
    mgr = SessionManager(inactivity_window=timedelta(minutes=30))
    session = mgr.open("user-1")
    assert mgr.is_active(session.id) is True


def test_session_expires_after_inactivity():
    mgr = SessionManager(inactivity_window=timedelta(seconds=0))
    session = mgr.open("user-1")
    # With a zero-length window, any elapsed time expires the session.
    assert mgr.is_active(session.id) is False


def test_unknown_session_is_inactive():
    mgr = SessionManager()
    assert mgr.is_active("does-not-exist") is False
