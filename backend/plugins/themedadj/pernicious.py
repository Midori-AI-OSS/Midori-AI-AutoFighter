from dataclasses import dataclass


@dataclass
class Pernicious:
    plugin_type = "themedadj"
    id = "pernicious"
    name = "Pernicious"

    def apply(self, target) -> None:
        target.max_hp = int(target.max_hp * 1.95)
        target.crit_rate = target.crit_rate + 0.05
