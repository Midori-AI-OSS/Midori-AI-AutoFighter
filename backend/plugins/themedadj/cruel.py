from dataclasses import dataclass


@dataclass
class Cruel:
    plugin_type = "themedadj"
    id = "cruel"
    name = "Cruel"

    def apply(self, target) -> None:
        target.crit_damage = target.crit_damage * 1.05
