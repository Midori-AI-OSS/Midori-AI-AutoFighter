from __future__ import annotations


def upgrade(conn):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS runs(
            id TEXT PRIMARY KEY,
            data BLOB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS players(
            id TEXT PRIMARY KEY,
            data BLOB NOT NULL
        );
        """
    )

