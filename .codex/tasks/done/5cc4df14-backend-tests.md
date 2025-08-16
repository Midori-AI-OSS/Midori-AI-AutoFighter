# Add backend tests for run and rooms (`5cc4df14`)

## Summary
Verify run creation, room transitions, and save persistence with automated tests.

## Tasks
- Write pytest cases covering run start, party updates, and room interactions.
- Ensure tests exercise the new battle, shop, and rest endpoints.
- Keep tests using `save.db` with env-driven path and key.

## Context
Prevents regressions in the web-based backend.
