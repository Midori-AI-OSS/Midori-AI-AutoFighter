# SaveManager

Wrapper around SQLCipher connections and database migrations.

## Migration safety
- Migration filenames must start with a numeric prefix (`NNN_description.sql`).
- Non-numeric prefixes are ignored to prevent executing unexpected scripts.
- `PRAGMA user_version` does not accept parameter binding; the version value is
  cast to `int` before being interpolated to avoid SQL injection.

## Backup and restore
- `GET /save/backup` exports the `runs`, `options`, and `damage_types` tables
  as JSON, hashes the plaintext payload with SHA-256, embeds the hash, then
  encrypts the package with Fernet using a key derived from the database key.
- `POST /save/restore` accepts the encrypted blob, decrypts and verifies the
  embedded hash, and repopulates the tables only if the digest matches.
- `POST /save/wipe` deletes the encrypted database file and reruns migrations,
  recreating `runs`, `owned_players`, `options`, and `damage_types`. A random
  starting persona (either LadyDarkness or LadyLight) is inserted into
  `owned_players` after migrations. Any new tables must have corresponding
  migrations so wipes rebuild them.
  `DELETE /run/<id>` removes a single active run without touching other data.

## Run snapshots
- `POST /run/start` clones the player's pronouns, damage type, and stat points
  into the run record so mid-run edits to the player editor do not change the
  active party.
