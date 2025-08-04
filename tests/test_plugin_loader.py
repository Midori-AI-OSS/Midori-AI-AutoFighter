import importlib
import sys

from pathlib import Path

try:
    importlib.import_module("direct.showbase.MessengerGlobal")
except ModuleNotFoundError:
    import pytest

    pytest.skip("Panda3D not available", allow_module_level=True)

sys.path.append(str(Path(__file__).resolve().parents[1]))

from plugins.event_bus import EventBus
from plugins.plugin_loader import PluginLoader


def test_discovers_plugins_and_injects_bus() -> None:
    bus = EventBus()
    loader = PluginLoader(bus)
    root = Path(__file__).resolve().parents[1] / "plugins"
    loader.discover(str(root))
    for category in [
        "dots",
        "hots",
        "passives",
        "players",
        "foes",
        "weapons",
        "rooms",
    ]:
        found = loader.get_plugins(category)
        assert found, f"{category} not loaded"
        for plugin in found.values():
            assert getattr(plugin, "bus") is bus
