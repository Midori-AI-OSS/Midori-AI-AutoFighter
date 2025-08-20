from dataclasses import dataclass


@dataclass
class Horrible:
    plugin_type = "themedadj"
    id = "horrible"
    name = "Horrible"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.02)
        target.crit_rate = target.crit_rate + 0.02
