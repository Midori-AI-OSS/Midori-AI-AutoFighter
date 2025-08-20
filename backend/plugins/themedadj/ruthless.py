from dataclasses import dataclass


@dataclass
class Ruthless:
    plugin_type = "themedadj"
    id = "ruthless"
    name = "Ruthless"

    def apply(self, target) -> None:
        target.crit_damage = target.crit_damage * 1.15
