from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from autofighter.passives import PassiveRegistry
from plugins import PluginLoader
from plugins.players.player import Player


def test_passive_discovery():
    loader = PluginLoader(required=["passive"])
    loader.discover(Path(__file__).resolve().parents[1] / "plugins" / "passives")
    passives = loader.get_plugins("passive")
    assert "attack_up" in passives


def test_passive_trigger_and_stack():
    registry = PassiveRegistry()
    player = Player()
    player.passives = ["attack_up"] * 5
    registry.trigger("battle_start", player)
    assert player.atk == 100 + 5 * 5


def test_room_heal_trigger():
    registry = PassiveRegistry()
    player = Player()
    player.hp = 900
    player.passives = ["room_heal"] * 10
    registry.trigger("battle_end", player)
    assert player.hp == 910
