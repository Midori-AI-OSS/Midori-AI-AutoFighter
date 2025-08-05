import sys
import logging
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from plugins.plugin_loader import PluginLoader


class DummyBus:
    pass


def test_discovers_plugins_and_injects_bus() -> None:
    bus = DummyBus()
    loader = PluginLoader(bus)
    root = Path(__file__).resolve().parents[1] / "plugins"
    loader.discover(str(root))
    for category in [
        "dot",
        "hot",
        "passive",
        "player",
        "foe",
        "weapon",
        "room",
    ]:
        found = loader.get_plugins(category)
        assert found, f"{category} not loaded"
        for plugin in found.values():
            assert getattr(plugin, "bus") is bus


def test_missing_category_raises_keyerror() -> None:
    loader = PluginLoader()
    with pytest.raises(KeyError):
        loader.get_plugins("missing")


def test_logs_import_errors(tmp_path, caplog) -> None:
    bad = tmp_path / "bad.py"
    bad.write_text("raise RuntimeError('boom')\n")
    loader = PluginLoader()
    with caplog.at_level(logging.ERROR):
        loader.discover(str(tmp_path))
    assert "bad.py" in caplog.text

