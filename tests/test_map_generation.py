import pytest

from autofighter.map_generation import MapGenerator

def test_floor_has_required_rooms(tmp_path):
    gen = MapGenerator(base_seed=123, seed_store_path=tmp_path / "seeds.json")
    nodes = gen.generate_floor(1)
    types = [n.room_type for n in nodes]
    assert len(nodes) == 45
    assert types[-1] == "battle_boss_floor"
    assert types.count("shop") >= 2
    assert types.count("rest") >= 2

def test_deterministic_seed(tmp_path):
    gen1 = MapGenerator(base_seed=42, seed_store_path=tmp_path / "a.json")
    gen2 = MapGenerator(base_seed=42, seed_store_path=tmp_path / "b.json")
    floor1 = gen1.generate_floor(1)
    floor2 = gen2.generate_floor(1)
    assert [n.room_type for n in floor1] == [n.room_type for n in floor2]

def test_pressure_level_adds_rooms_and_boss(tmp_path):
    gen = MapGenerator(base_seed=5, pressure_level=20, seed_store_path=tmp_path / "c.json")
    nodes = gen.generate_floor(1)
    assert len(nodes) == 47
    types = [n.room_type for n in nodes]
    assert types.count("battle_boss") >= 1


def test_three_starting_paths(tmp_path):
    gen = MapGenerator(base_seed=7, seed_store_path=tmp_path / "s.json")
    nodes = gen.generate_floor(1)
    assert nodes[0].links == [1, 2, 3]
    assert nodes[1].links == [4]
    assert nodes[2].links == [4]
    assert nodes[3].links == [4]


def test_duplicate_seed_detected(tmp_path):
    store = tmp_path / "seeds.json"
    MapGenerator(base_seed=99, seed_store_path=store)
    with pytest.raises(ValueError):
        MapGenerator(base_seed=99, seed_store_path=store)

