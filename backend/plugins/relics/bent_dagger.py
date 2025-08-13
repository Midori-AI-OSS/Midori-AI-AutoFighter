from dataclasses import dataclass
from dataclasses import field

from plugins.relics._base import RelicBase


@dataclass
class BentDagger(RelicBase):
    id: str = "bent_dagger"
    name: str = "Bent Dagger"
    effects: dict[str, float] = field(default_factory=lambda: {"atk": 0.03})

