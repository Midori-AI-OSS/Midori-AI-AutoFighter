import autofighter.effects as effects

import pytest

from autofighter.stats import Stats
from plugins.event_bus import EventBus
from autofighter.effects import EffectManager
from plugins.damage_types.fire import Fire


def test_dot_applies_with_hit_rate():
    attacker = Stats(atk=50, effect_hit_rate=2.0, base_damage_type=Fire())
    target = Stats(effect_resistance=0.0)
    manager = EffectManager(target)
    manager.maybe_inflict_dot(attacker, 50)
    assert target.dots


import pytest


@pytest.mark.asyncio
async def test_damage_and_heal_events():
    bus = EventBus()
    events = []

    def _dmg(target, attacker, amount):
        events.append(("dmg", amount))

    def _heal(target, healer, amount):
        events.append(("heal", amount))

    bus.subscribe("damage_taken", _dmg)
    bus.subscribe("heal_received", _heal)
    attacker = Stats(atk=10, base_damage_type=Fire())
    target = Stats(hp=50, max_hp=100)
    await target.apply_damage(10, attacker=attacker)
    await target.apply_healing(5, healer=attacker)
    bus.unsubscribe("damage_taken", _dmg)
    bus.unsubscribe("heal_received", _heal)
    assert ("dmg", 1) in events and ("heal", 5) in events


def test_dot_has_minimum_chance(monkeypatch):
    attacker = Stats(effect_hit_rate=0.0, base_damage_type=Fire())
    target = Stats(effect_resistance=5.0)
    manager = EffectManager(target)
    monkeypatch.setattr(effects.random, "uniform", lambda a, b: 1.0)
    monkeypatch.setattr(effects.random, "random", lambda: 0.0)
    manager.maybe_inflict_dot(attacker, 10)
    assert target.dots
