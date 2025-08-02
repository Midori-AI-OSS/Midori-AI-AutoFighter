import sys
import types
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.modules.setdefault("halo", types.SimpleNamespace(Halo=lambda **kwargs: None))


class _DummyFore:
    def __getattr__(self, name):
        return ""


sys.modules.setdefault(
    "colorama",
    types.SimpleNamespace(Fore=_DummyFore(), Style=types.SimpleNamespace(RESET_ALL="")),
)
sys.modules.setdefault("pygame", types.SimpleNamespace())

from player import Player, create_player
from plugins.plugin_loader import PluginLoader


def test_warrior_plugin_registered():
    loader = PluginLoader()
    loader.discover("plugins/players")
    plugins = loader.get_plugins("player")
    assert "warrior" in plugins


def test_create_player_uses_plugin():
    player = create_player("warrior", name="Hero")
    assert isinstance(player, Player)
    assert player.PlayerName == "Hero"


def test_create_player_fallback():
    player = create_player("unknown", name="Rogue")
    assert isinstance(player, Player)
    assert player.PlayerName == "Rogue"
