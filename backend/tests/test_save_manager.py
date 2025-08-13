import hashlib
from pathlib import Path

import pytest
import sqlcipher3

from autofighter.save_manager import SaveManager


def test_password_derives_key(tmp_path, monkeypatch):
    db_path = tmp_path / "save.db"
    migrations = Path(__file__).resolve().parents[1] / "migrations"
    monkeypatch.setenv("AF_DB_PATH", str(db_path))
    monkeypatch.setenv("AF_DB_PASSWORD", "secret")
    mgr = SaveManager.from_env()
    assert mgr.key == hashlib.sha256(b"secret").hexdigest()
    mgr.migrate(migrations)
    with mgr.connection() as conn:
        conn.execute(
            "INSERT INTO runs (id, party, map) VALUES ('1', '[]', '[]')"
        )
        version = conn.execute("PRAGMA user_version").fetchone()[0]
    assert version == 1
    mgr2 = SaveManager.from_env()
    with mgr2.connection() as conn:
        cur = conn.execute("SELECT COUNT(*) FROM runs")
        assert cur.fetchone()[0] == 1
    bad_mgr = SaveManager(db_path, "badkey")
    with pytest.raises(sqlcipher3.DatabaseError):
        with bad_mgr.connection() as conn:
            conn.execute("SELECT COUNT(*) FROM runs")
