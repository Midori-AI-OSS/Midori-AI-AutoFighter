from dataclasses import dataclass


@dataclass
class Scary:
    plugin_type = "themedadj"
    id = "scary"
    name = "Scary"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.95)
        target.dodge_odds = target.dodge_odds * 1.05
        target.crit_damage = target.crit_damage * 1.05
