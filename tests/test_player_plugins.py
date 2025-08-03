import sys
import types
import random
from pathlib import Path

import pytest

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

from items import ItemType
from player import Player, create_player
from plugins.plugin_loader import PluginLoader


PLAYER_IDS = [
    ("luna", "Luna"),
    ("carly", "Carly"),
    ("becca", "Becca"),
    ("ally", "Ally"),
    ("hilander", "Hilander"),
    ("chibi", "Chibi"),
    ("mimic", "Mimic"),
    ("mezzy", "Mezzy"),
    ("graygray", "Graygray"),
    ("bubbles", "Bubbles"),
    ("lady_light", "Lady Light"),
    ("lady_darkness", "Lady Darkness"),
    ("lady_of_fire", "Lady Of Fire"),
    ("lady_fire_and_ice", "Lady Fire And Ice"),
    ("lady_echo", "Lady Echo"),
    ("kboshi", "Kboshi"),
]


@pytest.mark.parametrize("player_id,_", PLAYER_IDS)
def test_player_plugin_registered(player_id, _):
    loader = PluginLoader()
    loader.discover("plugins/players")
    plugins = loader.get_plugins("player")
    assert player_id in plugins


@pytest.mark.parametrize("player_id, expected_name", PLAYER_IDS)
def test_create_player_uses_plugin(player_id, expected_name):
    player = create_player(player_id)
    assert isinstance(player, Player)
    assert player.PlayerName == expected_name
    assert player.isplayer is True


def test_create_player_fallback():
    player = create_player("unknown", name="Rogue")
    assert isinstance(player, Player)
    assert player.PlayerName == "Rogue"
    assert player.isplayer is True


def test_graygray_passive_applied():
    baseline = Player("Temp").Regain
    player = create_player("graygray")
    assert player.Regain == pytest.approx(baseline * 0.05 * player.level)


def test_ally_passive_applied():
    baseline = Player("Temp")
    player = create_player("ally")
    assert player.Atk == pytest.approx(int(baseline.Atk * 1.5))
    assert player.Def == pytest.approx(int(baseline.Def * 1.5))
    assert player.DodgeOdds == pytest.approx(baseline.DodgeOdds / 1000)
    assert player.CritDamageMod == pytest.approx(baseline.CritDamageMod * ((0.005 * player.level) + 1))


def test_bubbles_passive_applied():
    random.seed(0)
    plain = Player("Bubbles")
    plain.load()
    plain.set_photo("bubbles")
    plain.isplayer = True
    plain.Items.append(ItemType())
    baseline = plain.Items[0].power

    random.seed(0)
    player = create_player("bubbles")
    item = player.Items[0]
    assert item.name == "Bubbles's Blessing of Damage, Defense, and Utility"
    assert item.power == pytest.approx(baseline + player.level * 0.0003)


def test_carly_passive_applied():
    plain = Player("Carly")
    plain.load()
    plain.set_photo("carly")
    plain.isplayer = True
    baseline_def = plain.Def
    baseline_crit = plain.CritDamageMod

    player = create_player("carly")
    assert player.Atk == 1
    assert player.Def > baseline_def
    assert player.CritDamageMod > baseline_crit


def test_luna_passive_applied():
    baseline = Player("Temp")
    player = create_player("luna")
    assert player.MHP == pytest.approx(baseline.MHP / 4)
    assert player.Def == pytest.approx(int(baseline.Def * 2))
    expected_dodge = baseline.DodgeOdds + 1.1 * baseline.Vitality
    assert player.DodgeOdds == pytest.approx(expected_dodge)

