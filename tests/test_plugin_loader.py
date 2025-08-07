import sys
import logging

import pytest

from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from plugins.plugin_loader import PluginLoader


class DummyBus:
    pass


def test_discovers_plugins_and_injects_bus() -> None:
    bus = DummyBus()
    loader = PluginLoader(bus)
    root = Path(__file__).resolve().parents[1] / "plugins"
    mods_root = Path(__file__).resolve().parents[1] / "mods"
    loader.discover(str(root))
    loader.discover(str(mods_root))
    for category in [
        "dot",
        "hot",
        "passive",
        "player",
        "foe",
        "weapon",
        "room",
        "event",
    ]:
        found = loader.get_plugins(category)
        assert found, f"{category} not loaded"
        for plugin in found.values():
            assert getattr(plugin, "bus") is bus
    assert "mod_passive" in loader.get_plugins("passive")
    assert getattr(loader.get_plugins("passive")["mod_passive"], "bus") is bus


def test_missing_category_raises_runtimeerror() -> None:
    root = Path(__file__).resolve().parents[1] / "plugins"
    loader = PluginLoader(required={"missing"})
    with pytest.raises(RuntimeError):
        loader.discover(str(root))


def test_get_plugins_missing_category_runtimeerror() -> None:
    loader = PluginLoader()
    with pytest.raises(RuntimeError):
        loader.get_plugins("missing")


def test_logs_import_errors(tmp_path, caplog) -> None:
    bad = tmp_path / "bad.py"
    bad.write_text("raise RuntimeError('boom')\n")
    loader = PluginLoader()
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ImportError) as exc_info:
            loader.discover(str(tmp_path))
    assert "bad.py" in caplog.text
    assert "RuntimeError: boom" in str(exc_info.value)

