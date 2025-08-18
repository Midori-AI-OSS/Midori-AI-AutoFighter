import random

import pytest

from autofighter.party import Party
from autofighter.stats import Stats
from autofighter.rooms import BattleRoom
from autofighter.mapgen import MapNode
from plugins.foes._base import FoeBase
from plugins.players import player as player_mod


@pytest.mark.asyncio
async def test_battle_room_awards_exp(monkeypatch):
    node = MapNode(room_id=0, room_type="battle", floor=1, index=2, loop=1, pressure=0)
    room = BattleRoom(node)
    player = player_mod.Player()
    player.atk = 1000
    player.exp = 0
    party = Party(members=[player])

    class DummyFoe(FoeBase):
        id = "dummy"
        name = "Dummy"

    foe = DummyFoe()
    foe.hp = 1
    foe.level = 3
    monkeypatch.setattr("autofighter.rooms._choose_foe", lambda p: foe)
    monkeypatch.setattr("autofighter.rooms._scale_stats", lambda *args, **kwargs: None)
    result = await room.resolve(party, {})
    assert party.members[0].exp == 3 * 12 + 5 * 2
    assert result["room_number"] == 2
    assert result["exp_reward"] == 3 * 12 + 5 * 2


def test_gain_exp_and_level_up(monkeypatch):
    stats = Stats(hp=100, max_hp=100, atk=10, defense=5)
    monkeypatch.setattr(random, "uniform", lambda a, b: 0)
    stats.gain_exp(100)
    assert stats.level == 2
    assert stats.exp == 0
    assert stats.max_hp == 120
    assert stats.atk == 20
    assert stats.defense == 11
