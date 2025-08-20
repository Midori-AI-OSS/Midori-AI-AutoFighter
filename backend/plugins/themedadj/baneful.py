from dataclasses import dataclass


@dataclass
class Baneful:
    plugin_type = "themedadj"
    id = "baneful"
    name = "Baneful"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.95)
        target.crit_damage = target.crit_damage * 1.05
