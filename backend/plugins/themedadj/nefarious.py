from dataclasses import dataclass


@dataclass
class Nefarious:
    plugin_type = "themedadj"
    id = "nefarious"
    name = "Nefarious"

    def apply(self, target) -> None:
        target.crit_rate = target.crit_rate + 0.05
        target.crit_damage = target.crit_damage * 1.05
