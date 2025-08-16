# Parameterize SaveManager key PRAGMA (`3c4d5e6f`)

## Summary
The `SaveManager` used string formatting when applying the SQLCipher key, allowing crafted values to execute arbitrary SQL.

## Tasks
- [x] Replace string interpolation with parameterized execution in the PRAGMA `key` statement.
- [x] Add regression tests ensuring malformed keys cannot run raw SQL.
- [ ] Review remaining PRAGMA usage for similar injection risks.

## Context
Parameterizing the key ensures SQLite treats the provided value strictly as data, blocking injection vectors such as `"x'; DROP TABLE runs;--"`.
