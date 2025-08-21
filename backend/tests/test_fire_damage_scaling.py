import pytest

from autofighter.stats import Stats
from plugins.damage_types.fire import Fire


@pytest.mark.asyncio
async def test_fire_damage_increases_as_hp_drops():
    attacker = Stats(defense=0, base_damage_type=Fire())
    target_full = Stats(defense=0)
    dmg_full = await target_full.apply_damage(100, attacker)

    attacker.hp = attacker.max_hp // 2
    target_half = Stats(defense=0)
    dmg_half = await target_half.apply_damage(100, attacker)

    attacker.hp = 1
    target_low = Stats(defense=0)
    dmg_low = await target_low.apply_damage(100, attacker)

    assert dmg_full < dmg_half < dmg_low
