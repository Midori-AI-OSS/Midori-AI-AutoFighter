import sys
import types

from importlib import reload

from autofighter.player_creator import DAMAGE_TYPES
from autofighter.player_creator import PlayerCreator


class DummyApp:
    def __init__(self) -> None:
        self.scene_manager = object()


class _FakeCursor:
    def __init__(self, getter):
        self._getter = getter

    def fetchone(self):
        value = self._getter()
        return (value,) if value is not None else None


class _FakeConnection:
    storage = {"players": {}}

    def __init__(self, _path):
        pass

    def execute(self, sql, params=()):
        if sql.startswith("PRAGMA"):
            return self
        if sql.startswith("SELECT data FROM players"):
            data = self.storage["players"].get(params[0])
            return _FakeCursor(lambda: data)
        if sql.startswith("INSERT OR REPLACE INTO players"):
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


def test_player_creation_consumes_bonus_when_used(tmp_path) -> None:
    fake_module = types.SimpleNamespace(connect=lambda path: _FakeConnection(path))
    sys.modules["sqlcipher3"] = fake_module
    import autofighter.save as save_module
    reload(save_module)
    save_module.DB_PATH = tmp_path / "player.db"
    _FakeConnection.storage = {"players": {}}
    app = DummyApp()
    inventory = {t: 100 for t in DAMAGE_TYPES}
    creator = PlayerCreator(app, inventory=inventory)
    creator.sliders = {"hp": {"value": 51}, "atk": {"value": 50}, "defense": {"value": 0}}
    creator.confirm()
    loaded = save_module.load_player()
    assert loaded is not None
    _, _, _, _, stats, inv = loaded
    assert stats.hp == 151
    assert stats.atk == 15
    assert stats.defense == 10
    assert all(v == 0 for v in inv.values())


def test_player_creation_refunds_unspent_bonus(tmp_path) -> None:
    fake_module = types.SimpleNamespace(connect=lambda path: _FakeConnection(path))
    sys.modules["sqlcipher3"] = fake_module
    import autofighter.save as save_module
    reload(save_module)
    save_module.DB_PATH = tmp_path / "player.db"
    _FakeConnection.storage = {"players": {}}
    app = DummyApp()
    inventory = {t: 100 for t in DAMAGE_TYPES}
    creator = PlayerCreator(app, inventory=inventory)
    creator.sliders = {"hp": {"value": 50}, "atk": {"value": 50}, "defense": {"value": 0}}
    creator.confirm()
    loaded = save_module.load_player()
    assert loaded is not None
    _, _, _, _, stats, inv = loaded
    assert stats.hp == 150
    assert stats.atk == 15
    assert stats.defense == 10
    assert all(v == 100 for v in inv.values())


def test_confirm_rejects_missing_bonus_items(tmp_path) -> None:
    fake_module = types.SimpleNamespace(connect=lambda path: _FakeConnection(path))
    sys.modules["sqlcipher3"] = fake_module
    import autofighter.save as save_module
    reload(save_module)
    save_module.DB_PATH = tmp_path / "player.db"
    _FakeConnection.storage = {"players": {}}
    app = DummyApp()
    inventory = {t: 0 for t in DAMAGE_TYPES}
    creator = PlayerCreator(app, inventory=inventory)
    creator.helper_label = {"text": ""}
    creator.sliders = {"hp": {"value": 101}, "atk": {"value": 0}, "defense": {"value": 0}}
    creator.confirm()
    assert _FakeConnection.storage["players"] == {}
    assert creator.helper_label["text"] == "Need 4★ items for extra points"


def test_on_slider_change_clamps_to_total_points() -> None:
    app = DummyApp()
    creator = PlayerCreator(app)
    creator.sliders = {"hp": {"value": 60}, "atk": {"value": 60}, "defense": {"value": 0}}
    creator.on_slider_change("atk")
    assert creator.sliders["atk"]["value"] == 40
    assert sum(int(s["value"]) for s in creator.sliders.values()) == creator.total_points


def test_confirm_button_requires_base_points() -> None:
    app = DummyApp()
    creator = PlayerCreator(app)
    creator.confirm_button = {"state": "normal"}
    creator.sliders = {"hp": {"value": 50}, "atk": {"value": 40}, "defense": {"value": 0}}
    creator.update_remaining()
    assert creator.confirm_button["state"] == "disabled"
    creator.sliders["defense"] = {"value": 10}
    creator.update_remaining()
    assert creator.confirm_button["state"] == "normal"

