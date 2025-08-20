from dataclasses import dataclass


@dataclass
class Villainous:
    plugin_type = "themedadj"
    id = "villainous"
    name = "Villainous"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.05)
        target.dodge_odds = target.dodge_odds * 1.95
        target.crit_rate = target.crit_rate + 0.05
