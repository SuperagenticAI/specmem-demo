"""Session storage and inactivity expiry.

See spec: .kiro/specs/session-auth (Requirement 1). The inactivity expiry behavior
here is protected by tests/auth/test_session_expiry.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone


DEFAULT_INACTIVITY_WINDOW = timedelta(minutes=30)


@dataclass
class Session:
    id: str
    user_id: str
    last_activity: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class SessionManager:
    """The only component that touches session storage."""

    def __init__(self, inactivity_window: timedelta | None = None) -> None:
        # Use `is None` rather than `or`: a zero timedelta is falsy but valid.
        if inactivity_window is None:
            inactivity_window = DEFAULT_INACTIVITY_WINDOW
        self._window = inactivity_window
        self._sessions: dict[str, Session] = {}

    def open(self, user_id: str) -> Session:
        session = Session(id=f"sess-{len(self._sessions) + 1}", user_id=user_id)
        self._sessions[session.id] = session
        return session

    def touch(self, session_id: str) -> None:
        """Record activity, resetting the inactivity timer."""
        if session_id in self._sessions:
            self._sessions[session_id].last_activity = datetime.now(timezone.utc)

    def is_active(self, session_id: str) -> bool:
        """Return True only if the session exists and is within the inactivity window."""
        session = self._sessions.get(session_id)
        if session is None:
            return False
        if datetime.now(timezone.utc) - session.last_activity > self._window:
            del self._sessions[session_id]
            return False
        return True
