import sys
import types

from pathlib import Path
from importlib import reload


class _FakeCursor:
    def __init__(self, getter):
        self._getter = getter

    def fetchone(self):
        value = self._getter()
        return (value,) if value is not None else None


class _FakeConnection:
    storage = {"runs": {}, "players": {}}

    def __init__(self, _path):
        pass

    def execute(self, sql, params=()):
        if sql.startswith("PRAGMA"):
            return self
        if sql.startswith("SELECT data FROM runs"):
            data = self.storage["runs"].get(params[0])
            return _FakeCursor(lambda: data)
        if sql.startswith("SELECT data FROM players"):
            data = self.storage["players"].get(params[0])
            return _FakeCursor(lambda: data)
        if sql.startswith("INSERT OR REPLACE INTO runs"):
            self.storage["runs"][params[0]] = params[1]
        elif sql.startswith("INSERT OR REPLACE INTO players"):
            self.storage["players"][params[0]] = params[1]
        return self

    def executescript(self, _script):
        return None

    def cursor(self):
        return self

    def fetchone(self):
        return None

    def close(self):
        return None

    def rollback(self):
        return None


def test_save_manager_batches_and_commits():
    fake_module = types.SimpleNamespace(connect=lambda path: _FakeConnection(path))
    sys.modules["sqlcipher3"] = fake_module
    from autofighter.saves import encrypted_store

    reload(encrypted_store)
    path = Path("test.db")

    with encrypted_store.SaveManager(path, "k") as sm:
        sm.queue_run("r", {"hp": 5})
        assert sm.fetch_run("r") is None
        sm.commit()
        assert sm.fetch_run("r") == {"hp": 5}

    with encrypted_store.SaveManager(path, "k") as sm:
        assert sm.fetch_run("r") == {"hp": 5}
        sm.queue_player("p", {"name": "Hero"})

    with encrypted_store.SaveManager(path, "k") as sm:
        assert sm.fetch_player("p") == {"name": "Hero"}
