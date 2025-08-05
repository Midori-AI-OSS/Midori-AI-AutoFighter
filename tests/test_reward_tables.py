from autofighter.rewards import WeightedPool
from autofighter.rewards import select_rewards

class DummyRng:
    def __init__(self, values: list[float]):
        self._values = iter(values)

    def random(self) -> float:
        return next(self._values)

    def uniform(self, a: float, b: float) -> float:
        return (a + b) / 2


def test_weighted_pool_selection():
    pool = WeightedPool([("a", 1), ("b", 3)])
    rng = DummyRng([0.0, 0.75])
    assert pool.pick(rng) == "a"
    assert pool.pick(rng) == "b"


def test_normal_reward_relic_drop():
    rng = DummyRng([0.0, 0.0, 0.0, 0.0])
    reward = select_rewards(loop=1, rng=rng)
    assert reward.relic in {1, 2}
    assert reward.card in {1, 2}
    assert reward.upgrade in {1, 2}


def test_floor_boss_ticket_scaling():
    rng = DummyRng([0.0, 0.0, 0.0])
    reward = select_rewards(floor_boss=True, pressure=40, loop=2, rng=rng)
    assert reward.tickets == 5
    assert reward.relic == 3 or reward.relic == 4
