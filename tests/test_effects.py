import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from autofighter.stats import Stats
from plugins.dots.bleed import Bleed
from autofighter.effects import EffectManager
from plugins.dots.cold_wound import ColdWound
from plugins.dots.impact_echo import ImpactEcho
from plugins.hots.player_echo import PlayerEcho
from plugins.hots.player_heal import PlayerHeal
from plugins.dots.frozen_wound import FrozenWound
from plugins.dots.gale_erosion import GaleErosion
from plugins.hots.regeneration import Regeneration
from plugins.dots.charged_decay import ChargedDecay
from plugins.dots.twilight_decay import TwilightDecay
from plugins.dots.blazing_torment import BlazingTorment
from plugins.dots.abyssal_weakness import AbyssalWeakness
from plugins.dots.celestial_atrophy import CelestialAtrophy
from plugins.dots.abyssal_corruption import AbyssalCorruption


def test_bleed_percent_damage() -> None:
    stats = Stats(hp=100, max_hp=100)
    mgr = EffectManager(stats)
    mgr.add_dot(Bleed(0, 1))
    mgr.tick()
    assert stats.hp == 98


def test_celestial_atrophy_reduces_atk() -> None:
    stats = Stats(hp=100, max_hp=100, atk=5)
    mgr = EffectManager(stats)
    mgr.add_dot(CelestialAtrophy(1, 1))
    mgr.tick()
    assert stats.atk == 4


def test_abyssal_corruption_spreads_on_death() -> None:
    one = Stats(hp=5, max_hp=100)
    two = Stats(hp=100, max_hp=100)
    m1 = EffectManager(one)
    m2 = EffectManager(two)
    m1.add_dot(AbyssalCorruption(10, 1))
    m1.tick(others=[m2])
    assert len(m2.dots) == 1


def test_abyssal_weakness_restores_defense() -> None:
    stats = Stats(hp=100, max_hp=100, defense=5)
    mgr = EffectManager(stats)
    mgr.add_dot(AbyssalWeakness(1, 1))
    mgr.tick()
    assert stats.defense == 5


def test_gale_erosion_strips_mitigation() -> None:
    stats = Stats(hp=100, max_hp=100, mitigation=5)
    mgr = EffectManager(stats)
    mgr.add_dot(GaleErosion(1, 1))
    mgr.tick()
    assert stats.mitigation == 4


def test_charged_decay_stuns_on_expire() -> None:
    stats = Stats(hp=100, max_hp=100)
    mgr = EffectManager(stats)
    mgr.add_dot(ChargedDecay(1, 1))
    mgr.tick()
    assert stats.stunned is True


def test_frozen_wound_reduces_actions_per_turn() -> None:
    stats = Stats(hp=100, max_hp=100, actions_per_turn=2)
    mgr = EffectManager(stats)
    mgr.add_dot(FrozenWound(1, 1))
    mgr.tick()
    assert stats.actions_per_turn == 1


def test_blazing_torment_extra_tick_on_action() -> None:
    stats = Stats(hp=100, max_hp=100)
    mgr = EffectManager(stats)
    effect = BlazingTorment(5, 2)
    mgr.add_dot(effect)
    mgr.tick()
    mgr.on_action()
    assert stats.hp == 90


def test_cold_wound_stack_limit() -> None:
    stats = Stats(hp=100, max_hp=100)
    mgr = EffectManager(stats)
    for _ in range(6):
        mgr.add_dot(ColdWound(1, 1))
    assert len([d for d in mgr.dots if d.id == "cold_wound"]) == 5


def test_twilight_decay_drains_vitality() -> None:
    stats = Stats(hp=100, max_hp=100, vitality=5.0)
    mgr = EffectManager(stats)
    mgr.add_dot(TwilightDecay(1, 1))
    mgr.tick()
    assert stats.vitality == 4.5


def test_impact_echo_repeats_last_hit() -> None:
    stats = Stats(hp=100, max_hp=100)
    stats.last_damage_taken = 40
    mgr = EffectManager(stats)
    mgr.add_dot(ImpactEcho())
    mgr.tick()
    assert stats.hp == 80


def test_regeneration_heals() -> None:
    stats = Stats(hp=90, max_hp=100)
    mgr = EffectManager(stats)
    mgr.add_hot(Regeneration(5, 1))
    mgr.tick()
    assert stats.hp == 95


def test_player_echo_heals_fraction_of_damage() -> None:
    stats = Stats(hp=90, max_hp=100)
    effect = PlayerEcho("Test", 0, 1)
    effect.tick(stats, damage=50)
    assert stats.hp == 100


def test_player_heal_instant_and_over_time() -> None:
    stats = Stats(hp=80, max_hp=100)
    mgr = EffectManager(stats)
    mgr.add_hot(PlayerHeal("Test", 5, 2))
    mgr.tick()
    mgr.tick()
    assert stats.hp == 87


def test_stats_lists_track_effects() -> None:
    stats = Stats(hp=100, max_hp=100)
    mgr = EffectManager(stats)
    mgr.add_dot(Bleed(0, 1))
    mgr.add_hot(Regeneration(5, 1))
    assert stats.dots == ["Bleed"]
    assert stats.hots == ["Regeneration"]
    mgr.tick()
    assert stats.dots == []
    assert stats.hots == []

