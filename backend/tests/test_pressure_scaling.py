import pytest

from autofighter.mapgen import MapNode
from autofighter.party import Party
from autofighter.rooms import BattleRoom
from autofighter.rooms import _build_foes
from autofighter.stats import Stats


@pytest.mark.parametrize(
    "pressure,expected",
    [(0, 1), (5, 2), (25, 6), (50, 10)],
)
def test_build_foes_pressure(pressure, expected) -> None:
    node = MapNode(
        room_id=0,
        room_type="battle-normal",
        floor=1,
        index=1,
        loop=1,
        pressure=pressure,
    )
    player = Stats(hp=10, max_hp=10, atk=1, defense=1)
    player.id = "p1"
    party = Party(members=[player])
    foes = _build_foes(node, party)
    assert len(foes) == expected


@pytest.mark.asyncio
async def test_multi_foe_battle(monkeypatch) -> None:
    node = MapNode(
        room_id=0,
        room_type="battle-normal",
        floor=1,
        index=1,
        loop=1,
        pressure=10,
    )
    room = BattleRoom(node)
    player = Stats(hp=100, max_hp=100, atk=50, defense=1, mitigation=1.0)
    player.id = "p1"
    party = Party(members=[player])

    def build(node, party):
        foes = []
        for i in range(3):
            f = Stats(hp=10, max_hp=10, atk=1, defense=0)
            f.id = f"f{i}"
            foes.append(f)
        return foes

    monkeypatch.setattr("autofighter.rooms._build_foes", build)
    result = await room.resolve(party, {})
    assert len(result["foes"]) == 3
