# SQLCipher Save System

## Summary
Implement an encrypted save system using SQLCipher with salted passwords.

## Tasks
- [ ] Integrate SQLCipher to store run and player data with batched writes and compact schemas.
- [ ] Derive encryption keys from a user-supplied salted password and store them in encrypted config with optional cloud backup.
- [ ] Provide migration tooling for legacy saves using versioned scripts.
- [ ] Explore alternative key sources such as OS keyrings, environment variables, or hardware tokens.
- [ ] Wrap database access in a `SaveManager` with context-managed sessions.
- [ ] Document backup, recovery, and key management steps.

## Context
Encrypted saves protect player progress and enable cross-device transfers.

## Testing
- [ ] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.
