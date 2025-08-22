import pytest

from autofighter.party import Party
from autofighter.rooms import BattleRoom
from autofighter.stats import Stats
from autofighter.mapgen import MapNode
from plugins.damage_types._base import DamageTypeBase


class CancelDamage(DamageTypeBase):
    id = "Cancel"

    async def on_action(self, actor, allies, enemies):
        return False


@pytest.mark.asyncio
async def test_player_damage_type_cancels_attack():
    node = MapNode(
        room_id=0,
        room_type="battle-normal",
        floor=1,
        index=1,
        loop=1,
        pressure=0,
    )
    room = BattleRoom(node)
    player = Stats(
        hp=10,
        max_hp=10,
        defense=0,
        atk=5,
        damage_type=CancelDamage(),
    )
    player.id = "p1"
    foe = Stats(hp=10, max_hp=10, atk=1000, defense=0)
    foe.id = "f1"
    party = Party(members=[player])
    await room.resolve(party, {}, foe=foe)
    assert foe.hp == foe.max_hp


@pytest.mark.asyncio
async def test_foe_damage_type_cancels_attack():
    node = MapNode(
        room_id=0,
        room_type="battle-normal",
        floor=1,
        index=1,
        loop=1,
        pressure=0,
    )
    room = BattleRoom(node)
    player = Stats(atk=1000, defense=0)
    player.id = "p1"
    foe = Stats(hp=10, max_hp=10, atk=5, defense=0, damage_type=CancelDamage())
    foe.id = "f1"
    party = Party(members=[player])
    await room.resolve(party, {}, foe=foe)
    assert player.hp == player.max_hp
