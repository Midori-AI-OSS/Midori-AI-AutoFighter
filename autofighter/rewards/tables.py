from __future__ import annotations

import random

from dataclasses import dataclass
from typing import Generic
from typing import Sequence
from typing import TypeVar

T = TypeVar("T")


class WeightedPool(Generic[T]):
    def __init__(self, entries: Sequence[tuple[T, int]]) -> None:
        self.entries = list(entries)
        self.total = sum(weight for _, weight in self.entries)

    def pick(self, rng: random.Random) -> T:
        r = rng.random() * self.total
        upto = 0
        for item, weight in self.entries:
            upto += weight
            if r < upto:
                return item
        return self.entries[-1][0]


@dataclass
class Reward:
    gold: int
    upgrade: int
    card: int
    relic: int | None = None
    tickets: int = 0


@dataclass
class RewardConfig:
    normal_gold: int = 5
    boss_gold: int = 20
    floor_boss_gold: int = 200
    ticket_pressure_step: int = 20
    max_tickets: int = 5


config = RewardConfig()


RELIC_NORMAL = WeightedPool([(1, 98), (2, 2)])
UPGRADE_NORMAL = WeightedPool([(1, 80), (2, 20)])
CARD_NORMAL = WeightedPool([(1, 80), (2, 20)])

RELIC_BOSS = WeightedPool([(1, 40), (2, 30), (3, 15), (4, 10), (5, 5)])
UPGRADE_BOSS = WeightedPool([(1, 60), (2, 30), (3, 10)])
CARD_BOSS = WeightedPool([(1, 40), (2, 30), (3, 15), (4, 10), (5, 5)])

RELIC_FLOOR_BOSS = WeightedPool([(3, 98), (4, 2)])
UPGRADE_FLOOR_BOSS = WeightedPool([(3, 80), (4, 20)])
CARD_FLOOR_BOSS = WeightedPool([(3, 60), (4, 25), (5, 15)])


def select_rewards(
    *,
    boss: bool = False,
    floor_boss: bool = False,
    loop: int = 0,
    pressure: int = 0,
    rng: random.Random | None = None,
) -> Reward:
    rng = rng or random.Random()
    loop = max(1, loop)
    if floor_boss:
        relic = RELIC_FLOOR_BOSS.pick(rng)
        upgrade = UPGRADE_FLOOR_BOSS.pick(rng)
        card = CARD_FLOOR_BOSS.pick(rng)
        gold = int(config.floor_boss_gold * loop * rng.uniform(2.05, 4.25))
        tickets = min(
            config.max_tickets,
            1 + pressure // config.ticket_pressure_step + loop,
        )
    elif boss:
        relic = RELIC_BOSS.pick(rng) if rng.random() < 0.25 else None
        upgrade = UPGRADE_BOSS.pick(rng)
        card = CARD_BOSS.pick(rng)
        gold = int(config.boss_gold * loop * rng.uniform(1.53, 2.25))
        tickets = 0
    else:
        relic = RELIC_NORMAL.pick(rng) if rng.random() < 0.05 else None
        upgrade = UPGRADE_NORMAL.pick(rng)
        card = CARD_NORMAL.pick(rng)
        gold = int(config.normal_gold * loop * rng.uniform(1.01, 1.25))
        tickets = 0
    return Reward(gold=gold, upgrade=upgrade, card=card, relic=relic, tickets=tickets)
