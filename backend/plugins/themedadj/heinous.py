from dataclasses import dataclass


@dataclass
class Heinous:
    plugin_type = "themedadj"
    id = "heinous"
    name = "Heinous"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.1)
        target.crit_damage = target.crit_damage * 1.1
