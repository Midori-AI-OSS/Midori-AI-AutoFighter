import game.ui.party_picker as pp
from autofighter.stats import Stats
from plugins.plugin_loader import PluginLoader


class DummyApp:
    def __init__(self) -> None:
        self.scene_manager = type("SM", (), {"switch_to": lambda self, scene: setattr(self, "scene", scene)})()
        self.events: dict[str, object] = {}

    def accept(self, name: str, func) -> None:
        self.events[name] = func

    def ignore(self, name: str) -> None:
        self.events.pop(name, None)


def test_party_picker_starts_run_with_selection() -> None:
    app = DummyApp()
    stats = Stats(hp=5, max_hp=5)
    loader = PluginLoader()
    loader.discover("plugins/players")
    roster = list(loader.get_plugins("player"))[:2]

    class DummyRunMap:
        def __init__(self, _app: object, player: Stats, party: list[str], _seed: object | None = None) -> None:
            self.player = player
            self.party = party

    pp.RunMap = DummyRunMap

    picker = pp.PartyPicker(app, stats, roster=roster)
    picker.setup()
    assert picker.char_ids == roster[: len(picker.char_ids)]
    first = picker.char_ids[0]
    picker.toggle(first)
    picker.start_run()
    assert isinstance(app.scene_manager.scene, DummyRunMap)
    assert app.scene_manager.scene.party == [first]
    picker.teardown()


def test_party_picker_limits_to_four() -> None:
    app = DummyApp()
    stats = Stats(hp=5, max_hp=5)
    loader = PluginLoader()
    loader.discover("plugins/players")
    roster = list(loader.get_plugins("player").keys())
    picker = pp.PartyPicker(app, stats, roster=roster)
    picker.setup()
    for pid in picker.char_ids[:5]:
        picker.toggle(pid)
    assert len(picker.selected) <= 4
    picker.teardown()


def test_party_picker_excludes_unowned() -> None:
    app = DummyApp()
    stats = Stats(hp=5, max_hp=5)
    loader = PluginLoader()
    loader.discover("plugins/players")
    all_ids = list(loader.get_plugins("player"))
    roster = all_ids[:1]
    picker = pp.PartyPicker(app, stats, roster=roster)
    picker.setup()
    assert picker.char_ids == roster
    picker.teardown()
