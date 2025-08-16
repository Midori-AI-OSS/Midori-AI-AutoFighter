# SaveManager

Wrapper around SQLCipher connections and database migrations.

## Migration safety
- Migration filenames must start with a numeric prefix (`NNN_description.sql`).
- Non-numeric prefixes are ignored to prevent executing unexpected scripts.
- `PRAGMA user_version` does not accept parameter binding; the version value is
  cast to `int` before being interpolated to avoid SQL injection.
