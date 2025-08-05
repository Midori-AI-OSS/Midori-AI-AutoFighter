# Encrypted Save System

## Setup
- Uses [SQLCipher](https://www.zetetic.net/sqlcipher/) via the `sqlcipher3-binary` package.
- Install dependencies with `uv add sqlcipher3-binary`.
- Saves are stored in `autofighter/saves/encrypted_store.py` using a context-managed `SaveManager`; `autofighter/saves/key_manager.py` derives and stores the SQLCipher key.

## Schema
- Compact tables:
  - `runs(id TEXT PRIMARY KEY, data BLOB NOT NULL)`
  - `players(id TEXT PRIMARY KEY, data BLOB NOT NULL)`

## SaveManager Usage
```python
from pathlib import Path
from autofighter.saves.encrypted_store import SaveManager

with SaveManager(Path("save.db"), "password") as sm:
    sm.queue_run('current', {'hp': 10})
    sm.queue_player('player', {'name': 'Hero'})
    run = sm.fetch_run('current')
    player = sm.fetch_player('player')
```
- `key_manager.derive_key(password, salt)` returns the hex key and salt. `save_salt` and `load_salt` persist the salt next to the database as `save.key`.
- Queued writes flush in a single transaction on context exit or `commit()`.
- Use `key_manager.backup_key_file(src, dest)` and `key_manager.restore_key_file(src, dest)` to copy or restore the salt file.
- High-level helpers in `autofighter/save.py` wrap `SaveManager` for run and player data.

## Recovery
- If a session exits with an exception, pending writes roll back.
- Lost passwords or salts require restoring from backups; without both the database cannot be decrypted.
