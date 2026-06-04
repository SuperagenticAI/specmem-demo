# Design Document: Legacy DB Sessions (DEPRECATED)

## Overview

This design stored sessions as rows in a synchronous `sessions` table, written and read
directly by request handlers. It coupled handlers to the database and made inactivity
expiry hard to enforce consistently.

## Why it was replaced

- Handlers wrote to the database on the hot path, adding latency and lock contention.
- Expiry logic was duplicated across handlers, so sessions sometimes outlived their
  intended lifetime.

## Status

**Deprecated.** Superseded by `session-auth`, which centralizes session state and
inactivity expiry in `SessionManager`. Do not extend this design.
