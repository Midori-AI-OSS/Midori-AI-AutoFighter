from dataclasses import dataclass


@dataclass
class Foul:
    plugin_type = "themedadj"
    id = "foul"
    name = "Foul"

    def apply(self, target) -> None:
        target.defense = int(target.defense * 1.95)
        target.dodge_odds = target.dodge_odds * 1.95
