import sys
import types

from importlib import reload

from autofighter.stats import Stats


class _FakeCursor:
    def __init__(self, getter):
        self._getter = getter

    def fetchone(self):
        value = self._getter()
        return (value,) if value is not None else None


class _FakeConnection:
    storage = {"runs": {}, "players": {}}
    user_version = 0
    migrations_run = 0

    def __init__(self, _path):
        pass

    def execute(self, sql, params=()):
        if sql.startswith("PRAGMA user_version ="):
            type(self).user_version = int(sql.split("=")[1])
            return self
        if sql == "PRAGMA user_version":
            return _FakeCursor(lambda: type(self).user_version)
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
        type(self).migrations_run += 1
        return None

    def cursor(self):
        return self

    def fetchone(self):
        return None

    def close(self):
        return None

    def rollback(self):
        return None


def test_save_manager_batches_and_commits(tmp_path):
    fake_module = types.SimpleNamespace(connect=lambda path: _FakeConnection(path))
    sys.modules["sqlcipher3"] = fake_module
    from autofighter.saves import encrypted_store

    reload(encrypted_store)
    path = tmp_path / "test.db"

    with encrypted_store.SaveManager(path, "pw") as sm:
        sm.queue_run("r", {"hp": 5})
        assert sm.fetch_run("r") is None
        sm.commit()
        assert sm.fetch_run("r") == {"hp": 5}

    with encrypted_store.SaveManager(path, "pw") as sm:
        assert sm.fetch_run("r") == {"hp": 5}
        sm.queue_player("p", {"name": "Hero"})

    with encrypted_store.SaveManager(path, "pw") as sm:
        assert sm.fetch_player("p") == {"name": "Hero"}


def test_key_manager_backup_and_restore(tmp_path):
    from autofighter.saves import key_manager

    key1, salt = key_manager.derive_key("pw")
    key2, _ = key_manager.derive_key("pw", salt)
    assert key1 == key2

    key_file = tmp_path / "conf.key"
    key_manager.save_salt(key_file, salt)
    backup = tmp_path / "conf.bak"
    key_manager.backup_key_file(key_file, backup)

    key_file.unlink()
    key_manager.restore_key_file(backup, key_file)
    restored_salt = key_manager.load_salt(key_file)
    key3, _ = key_manager.derive_key("pw", restored_salt)
    assert key1 == key3


def test_save_module_roundtrip(tmp_path):
    fake_module = types.SimpleNamespace(connect=lambda path: _FakeConnection(path))
    sys.modules["sqlcipher3"] = fake_module
    from autofighter.saves import encrypted_store
    reload(encrypted_store)
    from autofighter import save
    reload(save)

    db_path = tmp_path / "test.db"
    stats = Stats(hp=5, max_hp=5)
    save.save_player(
        "Athletic",
        "Short",
        "Black",
        "None",
        stats,
        {},
        password="pw",
        path=db_path,
    )

    loaded = save.load_player("pw", path=db_path)
    assert loaded is not None
    body, hair, hair_color, accessory, stats2, inventory = loaded
    assert body == "Athletic"
    assert stats2.hp == 5


def test_migration_runner_applies_scripts(tmp_path):
    fake_module = types.SimpleNamespace(connect=lambda path: _FakeConnection(path))
    sys.modules["sqlcipher3"] = fake_module
    from autofighter.saves import encrypted_store
    reload(encrypted_store)

    _FakeConnection.user_version = 0
    _FakeConnection.migrations_run = 0

    path = tmp_path / "test.db"
    with encrypted_store.SaveManager(path, "pw"):
        pass

    assert _FakeConnection.user_version == 1
    assert _FakeConnection.migrations_run == 1

    with encrypted_store.SaveManager(path, "pw"):
        pass

    assert _FakeConnection.user_version == 1
    assert _FakeConnection.migrations_run == 1

