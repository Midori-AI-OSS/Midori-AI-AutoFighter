from dataclasses import dataclass


@dataclass
class Frightening:
    plugin_type = "themedadj"
    id = "frightening"
    name = "Frightening"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.05)
        target.dodge_odds = target.dodge_odds * 1.95
