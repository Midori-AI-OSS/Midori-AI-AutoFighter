from dataclasses import dataclass


@dataclass
class Wrongful:
    plugin_type = "themedadj"
    id = "wrongful"
    name = "Wrongful"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.05)
        target.defense = int(target.defense * 1.95)
        target.crit_damage = target.crit_damage * 1.05
