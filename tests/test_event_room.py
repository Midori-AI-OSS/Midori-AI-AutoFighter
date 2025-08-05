import sys
import importlib

from pathlib import Path

try:
    importlib.import_module("direct.showbase.MessengerGlobal")
except ModuleNotFoundError:
    import pytest

    pytest.skip("Panda3D not available", allow_module_level=True)

sys.path.append(str(Path(__file__).resolve().parents[1]))

from autofighter.stats import Stats
from plugins.plugin_loader import PluginLoader


def test_event_deterministic() -> None:
    loader = PluginLoader()
    root = Path(__file__).resolve().parents[1] / "plugins"
    loader.discover(str(root))
    events = loader.get_plugins("event")
    builder = events["fountain"]
    event1 = builder.build(seed=1)
    stats1 = Stats(hp=5, max_hp=10)
    items1: dict[str, int] = {}
    msg1 = event1.resolve(0, stats1, items1)
    event2 = builder.build(seed=1)
    stats2 = Stats(hp=5, max_hp=10)
    items2: dict[str, int] = {}
    msg2 = event2.resolve(0, stats2, items2)
    assert msg1 == msg2
    assert stats1.hp == stats2.hp
