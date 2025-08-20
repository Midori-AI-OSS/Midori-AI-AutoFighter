from dataclasses import dataclass


@dataclass
class Psychopathic:
    plugin_type = "themedadj"
    id = "psychopathic"
    name = "Psychopathic"

    def apply(self, target) -> None:
        target.dodge_odds = target.dodge_odds * 1.9
        target.atk = int(target.atk * 1.1)
        target.crit_damage = target.crit_damage * 1.1
