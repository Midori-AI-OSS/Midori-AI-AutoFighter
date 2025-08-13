# Implement encrypted save system
Establish SQLCipher-backed persistence for run and player data. Parent: [Encrypted Save System Plan](../planning/43054f8b-encrypted-save-system-plan.md).

## Requirements
- Wrap SQLite access in a `SaveManager` using SQLCipher.
- Derive keys from user-supplied passwords or environment variables.
- Batch writes and expose migration scripts for forward-compatible schemas.

## Acceptance Criteria
- Game state reads and writes through `SaveManager` using encrypted tables.
- Tests verify key handling and a migration path.
