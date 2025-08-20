from dataclasses import dataclass


@dataclass
class Diabolical:
    plugin_type = "themedadj"
    id = "diabolical"
    name = "Diabolical"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.1)
        target.dodge_odds = target.dodge_odds * 1.9
