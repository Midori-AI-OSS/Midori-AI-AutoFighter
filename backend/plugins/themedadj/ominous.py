from dataclasses import dataclass


@dataclass
class Ominous:
    plugin_type = "themedadj"
    id = "ominous"
    name = "Ominous"

    def apply(self, target) -> None:
        target.crit_rate = target.crit_rate + 0.02
        target.crit_damage = target.crit_damage * 1.03
