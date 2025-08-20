from dataclasses import dataclass


@dataclass
class Inhumane:
    plugin_type = "themedadj"
    id = "inhumane"
    name = "Inhumane"

    def apply(self, target) -> None:
        target.crit_damage = target.crit_damage * 1.1
