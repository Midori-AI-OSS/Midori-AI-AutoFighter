import importlib.util

from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "plugins.plugin_loader", Path(__file__).resolve().parent.parent / "plugins" / "plugin_loader.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
PluginLoader = module.PluginLoader

def test_discover_registers_valid_plugins(tmp_path):
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()

    (plugin_dir / "good.py").write_text(
        "class Good:\n    plugin_type = 'player'\n"
    )
    (plugin_dir / "bad.py").write_text("class Bad:\n    pass\n")
    (plugin_dir / "error.py").write_text("raise ImportError('boom')\n")

    loader = PluginLoader()
    loader.discover(str(plugin_dir))

    players = loader.get_plugins("player")
    assert "Good" in players
    assert "Bad" not in players
    assert players["Good"].plugin_type == "player"
