from autofighter.effects import EffectManager
from autofighter.stats import BUS
from autofighter.stats import Stats
from plugins.damage_types.dark import Dark
import pytest


@pytest.mark.asyncio
async def test_shadow_siphon_persistence_and_stat_gain():
    dark = Dark()
    actor = Stats(atk=100, defense=100, damage_type=dark)
    ally = Stats()
    actor.id = "actor"
    ally.id = "ally"
    actor.effect_manager = EffectManager(actor)
    ally.effect_manager = EffectManager(ally)
    allies = [actor, ally]

    await dark.on_action(actor, allies, [])

    for member in allies:
        await member.effect_manager.tick()

    assert actor.atk > 100
    assert actor.defense > 100
    first = actor.atk

    for member in allies:
        await member.effect_manager.tick()

    for member in allies:
        assert any(d.id == "shadow_siphon" for d in member.effect_manager.dots)

    assert actor.atk > first


@pytest.mark.asyncio
async def test_shadow_siphon_clears_on_battle_end():
    dark = Dark()
    actor = Stats(damage_type=dark)
    ally = Stats()
    actor.id = "actor"
    ally.id = "ally"
    actor.effect_manager = EffectManager(actor)
    ally.effect_manager = EffectManager(ally)
    allies = [actor, ally]

    await dark.on_action(actor, allies, [])
    BUS.emit("battle_end", actor)

    for member in allies:
        assert "shadow_siphon" not in member.dots
        assert all(d.id != "shadow_siphon" for d in member.effect_manager.dots)
