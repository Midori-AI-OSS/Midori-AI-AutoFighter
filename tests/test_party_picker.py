from pathlib import Path

import pytest

pytest.importorskip("PIL")

import game.ui.party_picker as pp
from autofighter.stats import Stats
from game.actors import CharacterType
from plugins.plugin_loader import PluginLoader


class DummyApp:
    def __init__(self) -> None:
        self.scene_manager = type("SM", (), {"switch_to": lambda self, scene: setattr(self, "scene", scene)})()
        self.events: dict[str, object] = {}
        self.main_menu = type(
            "MM",
            (),
            {
                "show": lambda self: setattr(self, "shown", True),
                "edit_player": lambda self: setattr(self, "edited", True),
            },
        )()
        self.plugin_loader = PluginLoader()
        self.plugin_loader.discover("plugins/players")
        self.plugin_loader.discover("plugins/damage_types")

    def accept(self, name: str, func, extraArgs=None) -> None:  # noqa: N803 - matching Panda3D
        self.events[name] = (func, extraArgs)

    def ignore(self, name: str) -> None:
        self.events.pop(name, None)


def test_party_picker_starts_run_with_selection() -> None:
    app = DummyApp()
    stats = Stats(hp=5, max_hp=5)
    roster = list(app.plugin_loader.get_plugins("player"))[:2]

    class DummyRunMap:
        def __init__(self, _app: object, player: Stats, party: list[str], _seed: object | None = None) -> None:
            self.player = player
            self.party = party

    pp.RunMap = DummyRunMap

    picker = pp.PartyPicker(app, stats, roster=roster)
    picker.setup()
    assert picker.char_ids == ["player"] + roster[: len(roster)]
    first = picker.char_ids[1]
    picker.toggle(first)
    picker.start_run()
    assert isinstance(app.scene_manager.scene, DummyRunMap)
    assert app.scene_manager.scene.party == [first]
    picker.teardown()


def test_party_picker_limits_to_four() -> None:
    app = DummyApp()
    stats = Stats(hp=5, max_hp=5)
    roster = list(app.plugin_loader.get_plugins("player").keys())
    picker = pp.PartyPicker(app, stats, roster=roster)
    picker.setup()
    for pid in picker.char_ids[1:6]:
        picker.toggle(pid)
    assert len(picker.selected) <= 4
    picker.teardown()


def test_party_picker_excludes_unowned() -> None:
    app = DummyApp()
    stats = Stats(hp=5, max_hp=5)
    all_ids = list(app.plugin_loader.get_plugins("player"))
    roster = all_ids[:1]
    picker = pp.PartyPicker(app, stats, roster=roster)
    picker.setup()
    assert picker.char_ids == ["player"] + roster
    picker.teardown()


def test_party_picker_uses_fallback_icon_for_missing_image() -> None:
    app = DummyApp()
    stats = Stats(hp=5, max_hp=5)
    roster = ["ally"]
    picker = pp.PartyPicker(app, stats, roster=roster)
    picker.setup()
    image_path = picker.buttons["ally"]["image"]
    assert Path(image_path).parent.name == "fallbacks"
    picker.teardown()


def test_party_picker_hides_horizontal_scrollbar() -> None:
    app = DummyApp()
    stats = Stats(hp=5, max_hp=5)
    roster = ["ally"]
    picker = pp.PartyPicker(app, stats, roster=roster)
    picker.setup()
    assert picker.scroll.horizontalScroll.isHidden()
    picker.teardown()


def test_home_returns_to_menu() -> None:
    app = DummyApp()
    stats = Stats(hp=5, max_hp=5)
    picker = pp.PartyPicker(app, stats, roster=[])
    picker.home()
    assert getattr(app.scene_manager, "scene", None) is None
    assert getattr(app.main_menu, "shown", False)


def test_selecting_player_shows_stats() -> None:
    app = DummyApp()
    player_stats = Stats(hp=7, max_hp=7)
    roster = ["ally"]
    picker = pp.PartyPicker(app, player_stats, roster=roster)
    picker.setup()
    other = roster[0]
    picker.char_stats[other].char_type = CharacterType.B
    picker.select(other)
    assert picker.stat_labels["hp"]["text"] == "hp: 1000"
    assert picker.model_name == "body_b"
    picker.select("player")
    assert picker.stat_labels["hp"]["text"] == "hp: 7"
    assert picker.model_name == "body_c"
    picker.teardown()


def test_clicking_unset_player_opens_editor() -> None:
    app = DummyApp()
    unset_stats = Stats(hp=1, max_hp=1)
    picker = pp.PartyPicker(app, unset_stats, roster=[])
    picker.select("player")
    assert getattr(app.main_menu, "edited", False)


def test_party_picker_random_background() -> None:
    app = DummyApp()
    stats = Stats(hp=5, max_hp=5)
    picker = pp.PartyPicker(app, stats, roster=[])
    picker.setup()
    assert Path(picker.root["image"]).parent.name == "backgrounds"
    picker.teardown()
