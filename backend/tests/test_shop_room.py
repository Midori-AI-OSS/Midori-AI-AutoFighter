from autofighter.party import Party
from autofighter.rooms import ShopRoom
from autofighter.mapgen import MapNode
from plugins.players._base import PlayerBase


def test_shop_room_heals_and_tracks_inventory():
    node = MapNode(room_id=1, room_type="shop", floor=1, index=1, loop=1, pressure=0)
    room = ShopRoom(node)

    p1 = PlayerBase()
    p1.id = "p1"
    p1.max_hp = 200
    p1.hp = 50

    p2 = PlayerBase()
    p2.id = "p2"
    p2.max_hp = 600
    p2.hp = 100

    p3 = PlayerBase()
    p3.id = "p3"
    p3.max_hp = 50
    p3.hp = 25

    p4 = PlayerBase()
    p4.id = "p4"
    p4.max_hp = 150
    p4.hp = 150

    party = Party(members=[p1, p2, p3, p4], gold=100)

    room.resolve(party, {"cost": 20, "item": "amulet"})

    assert [m.hp for m in party.members] == [100, 150, 50, 150]
    assert party.gold == 80
    assert party.relics == ["amulet"]
