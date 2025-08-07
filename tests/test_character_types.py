from plugins import players
from autofighter.stats import Stats
from game.actors import CharacterType
from plugins.players import Bubbles, Chibi, Graygray


def test_stats_default_type() -> None:
    stats = Stats(hp=1, max_hp=1)
    assert stats.char_type is CharacterType.C


def test_player_plugins_have_type() -> None:
    for name in players.__all__:
        plugin = getattr(players, name)
        assert getattr(plugin, "char_type", None) in CharacterType


def test_specific_character_types() -> None:
    assert Bubbles.char_type is CharacterType.A
    assert Chibi.char_type is CharacterType.A
    assert Graygray.char_type is CharacterType.B
