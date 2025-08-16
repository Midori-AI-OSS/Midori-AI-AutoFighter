from dataclasses import fields
from dataclasses import dataclass

from plugins.foes._base import FoeBase


@dataclass
class Slime(FoeBase):
    id = "slime"
    name = "Slime"
    prompt: str = "Foe prompt placeholder"
    about: str = "Foe description placeholder"

    def __post_init__(self) -> None:  # noqa: D401 - short init
        super().__post_init__()
        for field in fields(FoeBase):
            value = getattr(self, field.name)
            if isinstance(value, (int, float)):
                setattr(self, field.name, type(value)(value * 0.1))
