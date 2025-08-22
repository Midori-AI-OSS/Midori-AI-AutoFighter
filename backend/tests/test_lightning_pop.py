import asyncio

import pytest

from autofighter.effects import DamageOverTime, EffectManager
from autofighter.stats import Stats
from plugins.damage_types.lightning import Lightning


@pytest.mark.asyncio
async def test_lightning_pop_damage_and_stacks():
    lightning = Lightning()
    attacker = Stats(atk=0, damage_type=lightning)
    attacker.id = "attacker"
    target = Stats(hp=100, max_hp=100, defense=1, mitigation=1.0, vitality=1.0)
    target.id = "target"
    target.effect_manager = EffectManager(target)

    dot1 = DamageOverTime("Test", 40, 3, "t1", attacker)
    dot2 = DamageOverTime("Test2", 20, 5, "t2", attacker)
    target.effect_manager.add_dot(dot1)
    target.effect_manager.add_dot(dot2)
    initial_turns = [d.turns for d in target.effect_manager.dots]
    initial_count = len(target.effect_manager.dots)
    start_hp = target.hp

    base = await target.apply_damage(0, attacker=attacker)
    await asyncio.sleep(0)
    dummy = Stats(hp=start_hp, max_hp=start_hp, defense=1, mitigation=1.0, vitality=1.0)
    dummy.id = "dummy"
    dmg1 = await dummy.apply_damage(int(dot1.damage * 0.25), attacker=attacker)
    dummy.hp = start_hp
    dmg2 = await dummy.apply_damage(int(dot2.damage * 0.25), attacker=attacker)
    expected = max(start_hp - base - dmg1 - dmg2, 0)
    assert target.hp == expected
    assert [d.turns for d in target.effect_manager.dots] == initial_turns
    assert len(target.effect_manager.dots) == initial_count
