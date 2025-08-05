from autofighter.balance.floor_boss import scale_mechanics
from autofighter.balance.floor_boss import scale_rewards
from autofighter.balance.floor_boss import scale_stats
from autofighter.stats import Stats


def test_scale_stats_increases_with_loop_and_pressure():
    base = Stats(hp=100, max_hp=100, atk=10, defense=5)
    low = scale_stats(base, loop=0, pressure=0)
    high = scale_stats(base, loop=1, pressure=10)
    assert high.hp > low.hp
    assert high.atk > low.atk


def test_scale_mechanics_escalates():
    base = scale_mechanics(loop=0, pressure=0)
    escalated = scale_mechanics(loop=3, pressure=4)
    assert escalated["attack_bonus"] > base["attack_bonus"]
    assert escalated["extra_actions"] >= base["extra_actions"]


def test_scale_rewards_grow():
    base = scale_rewards(100, loop=0, pressure=0)
    boosted = scale_rewards(100, loop=1, pressure=10)
    assert boosted["gold"] > base["gold"]
    assert boosted["tickets"] >= base["tickets"]
