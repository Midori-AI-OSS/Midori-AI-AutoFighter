from dataclasses import dataclass


@dataclass
class Treacherous:
    plugin_type = "themedadj"
    id = "treacherous"
    name = "Treacherous"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.05)
        target.dodge_odds = target.dodge_odds * 1.05
        target.crit_rate = target.crit_rate + 0.05
