from dataclasses import dataclass


@dataclass
class Wicked:
    plugin_type = "themedadj"
    id = "wicked"
    name = "Wicked"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.08)
        target.crit_damage = target.crit_damage * 1.02
