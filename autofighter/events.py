import random

from typing import Callable
from dataclasses import dataclass

from autofighter.stats import Stats


@dataclass
class EventOption:
    text: str
    effect: Callable[[Stats, dict[str, int], random.Random], str]


@dataclass
class Event:
    prompt: str
    options: list[EventOption]
    seed: int = 0

    def resolve(self, choice: int, stats: Stats, items: dict[str, int]) -> str:
        rng = random.Random(self.seed)
        return self.options[choice].effect(stats, items, rng)
