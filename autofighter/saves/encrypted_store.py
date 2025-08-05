from __future__ import annotations

import json
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Any

import sqlcipher3

from . import key_management

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs(
    id TEXT PRIMARY KEY,
    data BLOB NOT NULL
);
CREATE TABLE IF NOT EXISTS players(
    id TEXT PRIMARY KEY,
    data BLOB NOT NULL
);
"""


class SaveManager(AbstractContextManager):
    def __init__(self, path: Path, password: str, config_path: Path | None = None):
        self.path = path
        self.password = password
        self.config_path = config_path or path.with_suffix(".key")
        self.key: str | None = None
        self.conn: sqlcipher3.Connection | None = None
        self._queue: list[tuple[str, tuple[Any, ...]]] = []

    def __enter__(self) -> "SaveManager":
        if self.config_path.exists():
            salt = key_management.load_salt(self.config_path)
        else:
            salt = None
        self.key, salt = key_management.derive_key(self.password, salt)
        key_management.save_salt(self.config_path, salt)
        self.conn = sqlcipher3.connect(self.path)
        self.conn.execute(f"PRAGMA key = \"x'{self.key}'\"")
        self.conn.executescript(SCHEMA)
        return self

    def queue_run(self, run_id: str, data: dict[str, Any]) -> None:
        payload = json.dumps(data)
        self._queue.append(
            (
                "INSERT OR REPLACE INTO runs (id, data) VALUES (?, ?)",
                (run_id, payload),
            )
        )

    def queue_player(self, player_id: str, data: dict[str, Any]) -> None:
        payload = json.dumps(data)
        self._queue.append(
            (
                "INSERT OR REPLACE INTO players (id, data) VALUES (?, ?)",
                (player_id, payload),
            )
        )

    def fetch_run(self, run_id: str) -> dict[str, Any] | None:
        assert self.conn is not None
        row = self.conn.execute(
            "SELECT data FROM runs WHERE id = ?",
            (run_id,),
        ).fetchone()
        return json.loads(row[0]) if row else None

    def fetch_player(self, player_id: str) -> dict[str, Any] | None:
        assert self.conn is not None
        row = self.conn.execute(
            "SELECT data FROM players WHERE id = ?",
            (player_id,),
        ).fetchone()
        return json.loads(row[0]) if row else None

    def commit(self) -> None:
        if not self.conn or not self._queue:
            return
        cur = self.conn.cursor()
        cur.execute("BEGIN")
        for sql, params in self._queue:
            cur.execute(sql, params)
        cur.execute("COMMIT")
        self._queue.clear()

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.conn:
            if exc_type is None:
                self.commit()
            else:
                self.conn.rollback()
            self.conn.close()
            self.conn = None
        return False

    def backup_config(self, backup_path: Path) -> None:
        key_management.backup_config(self.config_path, backup_path)

    def restore_config(self, backup_path: Path) -> None:
        key_management.restore_config(backup_path, self.config_path)
