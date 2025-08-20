from dataclasses import dataclass


@dataclass
class Repulsive:
    plugin_type = "themedadj"
    id = "repulsive"
    name = "Repulsive"

    def apply(self, target) -> None:
        target.defense = int(target.defense * 1.9)
        target.dodge_odds = target.dodge_odds * 1.1
