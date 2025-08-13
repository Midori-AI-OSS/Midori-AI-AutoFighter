from dataclasses import dataclass
from dataclasses import fields

from plugins.players.player import Player


@dataclass
class Slime(Player):
    plugin_type = "foe"
    id = "slime"
    name = "Slime"

    def __post_init__(self) -> None:  # noqa: D401 - short init
        super().__post_init__()
        for field in fields(Player):
            value = getattr(self, field.name)
            if isinstance(value, (int, float)):
                setattr(self, field.name, type(value)(value * 0.1))
