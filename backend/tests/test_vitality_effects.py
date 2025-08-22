import pytest

from autofighter.stats import Stats
from autofighter.effects import DamageOverTime


@pytest.mark.asyncio
async def test_healing_scales_with_vitality():
    healer = Stats(vitality=2.0)
    target = Stats(hp=400, max_hp=1000, vitality=1.5)
    healed = await target.apply_healing(100, healer)
    expected = int(100 * healer.vitality * target.vitality)
    assert healed == expected
    assert target.hp == 400 + expected


@pytest.mark.asyncio
async def test_dot_scales_with_vitality():
    attacker = Stats(vitality=2.0)
    target_low = Stats(defense=1, vitality=1.0)
    target_high = Stats(defense=1, vitality=2.0)
    dot1 = DamageOverTime("bleed", 10, 1, "bleed", source=attacker)
    await dot1.tick(target_low)
    low_damage = target_low.last_damage_taken
    dot2 = DamageOverTime("bleed", 10, 1, "bleed", source=attacker)
    await dot2.tick(target_high)
    high_damage = target_high.last_damage_taken
    assert low_damage >= 1 and high_damage >= 1
    assert low_damage > high_damage
