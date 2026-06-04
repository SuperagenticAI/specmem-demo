# Design Document: Session Auth

## Overview

Session Auth implements token-based authentication with inactivity expiry. Request
handlers depend on a single `SessionManager` interface; the concrete store can change
without touching handlers. Access tokens are short-lived and refreshed via rotation.

## Architecture

- `AuthService` (`src/auth/service.py`): issues access tokens, validates them, and
  drives the refresh/rotation flow.
- `SessionManager` (`src/auth/session.py`): owns session records and the inactivity
  expiry logic. It is the only component that touches session storage.

## Key Decisions

### Decision: stateless access tokens, stateful sessions

Access tokens are stateless and short-lived (15 minutes). The server keeps a session
record only to track last activity and to support revocation. This keeps the hot path
cheap while still allowing inactivity expiry and forced logout.

### Decision: inactivity expiry lives in SessionManager

Expiry is enforced in `SessionManager`, not scattered across handlers. A request first
refreshes last-activity, then the manager evaluates the InactivityWindow. This is the
behavior protected by `tests/auth/test_session_expiry.py`.

### Decision: refresh tokens rotate on use

Each refresh rotates the RefreshToken and invalidates the previous value, so a leaked
refresh token is single-use.

## Testing Strategy

- `tests/auth/test_session_expiry.py` covers Requirement 1 (inactivity expiry and the
  401 on expired sessions). Any change to `src/auth/session.py` must keep this passing.

## Migration Note

The session store was previously a synchronous database table (see the
`legacy-db-sessions` spec). That approach is **deprecated**. Do not reintroduce
direct database writes from request handlers.
