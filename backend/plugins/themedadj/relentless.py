from dataclasses import dataclass


@dataclass
class Relentless:
    plugin_type = "themedadj"
    id = "relentless"
    name = "Relentless"

    def apply(self, target) -> None:
        target.dodge_odds = target.dodge_odds * 1.9
        target.atk = int(target.atk * 1.05)
        target.crit_rate = target.crit_rate + 0.05
