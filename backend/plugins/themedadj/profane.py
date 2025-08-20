from dataclasses import dataclass


@dataclass
class Profane:
    plugin_type = "themedadj"
    id = "profane"
    name = "Profane"

    def apply(self, target) -> None:
        target.max_hp = int(target.max_hp * 1.9)
        target.crit_damage = target.crit_damage * 1.1
