from autofighter.save import load_player
from autofighter.player_creator import DAMAGE_TYPES
from autofighter.player_creator import PlayerCreator


class DummyApp:
    def __init__(self) -> None:
        self.scene_manager = object()


def test_player_creation_consumes_bonus_when_used(tmp_path) -> None:
    import autofighter.save as save_module

    save_module.PLAYER_FILE = tmp_path / "player.json"
    app = DummyApp()
    inventory = {t: 100 for t in DAMAGE_TYPES}
    creator = PlayerCreator(app, inventory=inventory)
    creator.sliders = {"hp": {"value": 51}, "atk": {"value": 50}, "defense": {"value": 0}}
    creator.confirm()
    loaded = load_player()
    assert loaded is not None
    _, _, _, _, stats, inv = loaded
    assert stats.hp == 151
    assert stats.atk == 15
    assert stats.defense == 10
    assert all(v == 0 for v in inv.values())


def test_player_creation_refunds_unspent_bonus(tmp_path) -> None:
    import autofighter.save as save_module

    save_module.PLAYER_FILE = tmp_path / "player.json"
    app = DummyApp()
    inventory = {t: 100 for t in DAMAGE_TYPES}
    creator = PlayerCreator(app, inventory=inventory)
    creator.sliders = {"hp": {"value": 50}, "atk": {"value": 50}, "defense": {"value": 0}}
    creator.confirm()
    loaded = load_player()
    assert loaded is not None
    _, _, _, _, stats, inv = loaded
    assert stats.hp == 150
    assert stats.atk == 15
    assert stats.defense == 10
    assert all(v == 100 for v in inv.values())
