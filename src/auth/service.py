"""Authentication service: issues and validates short-lived access tokens.

See spec: .kiro/specs/session-auth (Requirements 2 and 3).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from src.auth.session import SessionManager


ACCESS_TOKEN_TTL = timedelta(minutes=15)


class AuthService:
    """Issues access tokens and drives the refresh/rotation flow."""

    def __init__(self, sessions: SessionManager) -> None:
        self._sessions = sessions

    def issue_access_token(self, user_id: str) -> dict:
        """Issue a short-lived access token and open a session."""
        session = self._sessions.open(user_id)
        expires_at = datetime.now(timezone.utc) + ACCESS_TOKEN_TTL
        return {"user_id": user_id, "session_id": session.id, "expires_at": expires_at}

    def validate(self, session_id: str) -> bool:
        """Validate a request against its session, enforcing inactivity expiry."""
        return self._sessions.is_active(session_id)
