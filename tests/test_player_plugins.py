from pathlib import Path

from plugins import players
from plugins.plugin_loader import PluginLoader


def test_all_player_plugins_loaded() -> None:
    loader = PluginLoader()
    root = Path(__file__).resolve().parents[1] / "plugins"
    loader.discover(str(root))
    player_plugins = loader.get_plugins("player")
    for name in players.__all__:
        cls = getattr(players, name)
        assert cls.id in player_plugins
