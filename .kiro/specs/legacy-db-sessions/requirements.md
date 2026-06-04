# Requirements Document

## Introduction

Legacy DB Sessions describes the original session design, where request handlers wrote
session rows directly to a synchronous database table. It is retained for historical
context only. This approach is **deprecated** and superseded by the `session-auth` spec.

## Glossary

- **SessionRow**: A row in the `sessions` table representing one active session.

## Requirements

### Requirement 1: Sessions persisted as database rows (DEPRECATED)

**User Story:** As a developer, I wanted sessions stored as database rows, so that they
survived restarts.

#### Acceptance Criteria

1. WHEN a user logs in THEN the handler SHALL insert a SessionRow directly.
2. WHEN a request arrives THEN the handler SHALL read and update the SessionRow inline.

> DEPRECATED: direct database writes from handlers are no longer allowed. Use
> `SessionManager` from the `session-auth` spec instead.
