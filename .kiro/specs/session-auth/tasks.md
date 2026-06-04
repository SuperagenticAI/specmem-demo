# Implementation Plan

- [x] 1. Define the `SessionManager` interface in `src/auth/session.py`
  - Encapsulate session records and last-activity tracking
  - _Requirements: 3.1, 3.2_

- [x] 2. Implement inactivity expiry in `SessionManager`
  - Default InactivityWindow to 30 minutes when unset
  - Reject expired sessions with 401
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 3. Implement access-token issuance and validation in `src/auth/service.py`
  - 15-minute access-token lifetime
  - _Requirements: 2.1_

- [ ] 4. Implement refresh-token rotation in `src/auth/service.py`
  - Rotate and invalidate the previous refresh token on use
  - _Requirements: 2.2, 2.3_

- [x] 5. Cover inactivity expiry with `tests/auth/test_session_expiry.py`
  - _Requirements: 1.1, 1.2_
