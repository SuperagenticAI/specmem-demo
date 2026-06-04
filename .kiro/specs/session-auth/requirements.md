# Requirements Document

## Introduction

Session Auth provides token-based authentication for the API. It issues short-lived
access tokens, refreshes them safely, and expires inactive sessions so that a stolen
or abandoned token cannot be used indefinitely. These requirements define the behavior
that the implementation in `src/auth/service.py` and `src/auth/session.py` must protect.

## Glossary

- **AccessToken**: A short-lived credential presented on each request.
- **Session**: Server-side record tracking a user's authenticated state and last activity.
- **InactivityWindow**: The maximum idle time before a session expires.
- **RefreshToken**: A longer-lived credential used to mint new access tokens.

## Requirements

### Requirement 1: Sessions expire after inactivity

**User Story:** As a security engineer, I want sessions to expire after a period of
inactivity, so that an unattended or stolen token cannot be reused indefinitely.

#### Acceptance Criteria

1. WHEN a session has no activity for the configured InactivityWindow THEN the system SHALL mark the session expired.
2. WHEN a request presents a token for an expired session THEN the system SHALL reject it with 401.
3. WHEN a session receives a valid request THEN the system SHALL update its last-activity timestamp.
4. WHEN the InactivityWindow is unset THEN the system SHALL default to 30 minutes.

### Requirement 2: Access tokens are short-lived and refreshable

**User Story:** As an API consumer, I want short-lived access tokens with a refresh
flow, so that compromised tokens have a small blast radius.

#### Acceptance Criteria

1. WHEN an access token is issued THEN the system SHALL set its lifetime to 15 minutes.
2. WHEN a valid RefreshToken is presented THEN the system SHALL issue a new access token without re-authentication.
3. WHEN a RefreshToken is used THEN the system SHALL rotate it and invalidate the previous one.

### Requirement 3: Session storage is isolated from request handlers

**User Story:** As a maintainer, I want session storage behind a single interface, so
that the storage backend can change without touching request handlers.

#### Acceptance Criteria

1. WHEN a handler needs session state THEN it SHALL access it only through `SessionManager`.
2. WHEN the storage backend changes THEN request handlers SHALL require no modification.
