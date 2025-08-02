import importlib.util

from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "plugins.dots.poison", Path(__file__).resolve().parent.parent / "plugins" / "dots" / "poison.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Poison = module.Poison


class DummyTarget:
    def __init__(self, hp: int = 100) -> None:
        self.HP = hp


def test_poison_deals_damage_over_time():
    target = DummyTarget()
    dot = Poison(damage=10, turns=2)
    starting_hp = target.HP

    assert dot.tick(target, 1) is True
    assert target.HP == starting_hp - 10

    assert dot.tick(target, 1) is False
    assert target.HP == starting_hp - 20
