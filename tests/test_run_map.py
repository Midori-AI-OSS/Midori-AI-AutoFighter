import sys
import types

from pathlib import Path

from game.ui.run_map import RunMap
from autofighter.stats import Stats


class DummyApp:
    def __init__(self) -> None:
        self.scene_manager = type("SM", (), {"switch_to": lambda self, scene: setattr(self, "scene", scene)})()
        self.events: dict[str, object] = {}

    def accept(self, name: str, func) -> None:
        self.events[name] = func

    def ignore(self, name: str) -> None:
        self.events.pop(name, None)


def test_run_map_enters_battle(tmp_path: Path) -> None:
    app = DummyApp()
    stats = Stats(hp=5, max_hp=5)

    class DummyBattle:
        def __init__(self, *_, player: Stats, party: list[str], **__):
            self.player = player
            self.party = party

    sys.modules['autofighter.battle_room'] = types.SimpleNamespace(BattleRoom=DummyBattle)
    run_map = RunMap(app, stats, ["ally"], seed_store_path=tmp_path / "seeds.json")
    run_map.setup()
    assert run_map.label is not None
    assert "00:" in run_map.label["text"]
    assert "-> 01,02,03" in run_map.label["text"]

    run_map.enter_first_room()
    assert isinstance(app.scene_manager.scene, DummyBattle)
    assert app.scene_manager.scene.player is stats
    assert app.scene_manager.scene.party == ["ally"]
    run_map.teardown()
    del sys.modules['autofighter.battle_room']
