# Save Key Management

## Summary
Derive and back up encryption keys for SQLCipher saves.

## Tasks
- [ ] Generate keys from a salted user password.
- [ ] Store a backup copy in a secure location.
- [ ] Rotate keys and re-encrypt saves when the password changes.
- [ ] Document this feature in `.codex/implementation`.
- [ ] Add unit tests covering success and failure cases.

## Context
Secure key handling protects encrypted save data from loss or compromise.

## Testing
- [ ] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.
status: in progress
