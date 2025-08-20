from dataclasses import dataclass


@dataclass
class Dangerous:
    plugin_type = "themedadj"
    id = "dangerous"
    name = "Dangerous"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.05)
        target.crit_rate = target.crit_rate + 0.05
