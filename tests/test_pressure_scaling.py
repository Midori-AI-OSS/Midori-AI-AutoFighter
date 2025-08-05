from autofighter.stats import Stats
from autofighter.map_generation import MapGenerator
from autofighter.balance.pressure import apply_pressure


def test_apply_pressure_scales_stats():
    base = Stats(hp=100, max_hp=100, atk=10, defense=5)
    scaled = apply_pressure(base, 10)
    assert scaled.hp == 150
    assert scaled.atk == 15
    assert scaled.defense == 7


def test_pressure_affects_rooms_branches_bosses(tmp_path):
    gen = MapGenerator(base_seed=7, pressure_level=45, seed_store_path=tmp_path / "s.json")
    nodes = gen.generate_floor(1)
    assert len(nodes) == 49
    branch_nodes = [n for n in nodes if len(n.links) > 1]
    assert len(branch_nodes) == 3
    types = [n.room_type for n in nodes]
    assert types.count("battle_boss") == 2
