from autofighter.map_generation import MapGenerator

def test_floor_has_required_rooms():
    gen = MapGenerator(base_seed=123)
    nodes = gen.generate_floor(1)
    types = [n.room_type for n in nodes]
    assert len(nodes) == 45
    assert types[-1] == "battle_boss_floor"
    assert types.count("shop") >= 2
    assert types.count("rest") >= 2

def test_deterministic_seed():
    gen1 = MapGenerator(base_seed=42)
    gen2 = MapGenerator(base_seed=42)
    floor1 = gen1.generate_floor(1)
    floor2 = gen2.generate_floor(1)
    assert [n.room_type for n in floor1] == [n.room_type for n in floor2]

def test_pressure_level_adds_rooms_and_boss():
    gen = MapGenerator(base_seed=5, pressure_level=20)
    nodes = gen.generate_floor(1)
    assert len(nodes) == 47
    types = [n.room_type for n in nodes]
    assert types.count("battle_boss") >= 1

