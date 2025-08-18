import pytest
import autofighter.rooms as rooms_module
from autofighter.mapgen import MapNode
from autofighter.party import Party
from autofighter.stats import Stats


@pytest.mark.asyncio
async def test_battle_offers_relic_choices(monkeypatch):
    node = MapNode(room_id=1, room_type="battle-normal", floor=1, index=1, loop=1, pressure=0)
    room = rooms_module.BattleRoom(node)
    member = Stats()
    member.id = "p1"
    party = Party(members=[member])
    monkeypatch.setattr(rooms_module, "card_choices", lambda *args, **kwargs: [])
    monkeypatch.setattr(rooms_module.random, "random", lambda: 0.0)
    result = await room.resolve(party, {})
    assert len(result["relic_choices"]) == 3
