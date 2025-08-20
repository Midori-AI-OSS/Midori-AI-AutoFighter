from dataclasses import dataclass


@dataclass
class Cunning:
    plugin_type = "themedadj"
    id = "cunning"
    name = "Cunning"

    def apply(self, target) -> None:
        target.dodge_odds = target.dodge_odds * 1.1
