from dataclasses import dataclass


@dataclass
class Vicious:
    plugin_type = "themedadj"
    id = "vicious"
    name = "Vicious"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.1)
        target.crit_rate = target.crit_rate + 0.05
