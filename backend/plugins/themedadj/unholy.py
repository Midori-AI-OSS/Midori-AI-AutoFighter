from dataclasses import dataclass


@dataclass
class Unholy:
    plugin_type = "themedadj"
    id = "unholy"
    name = "Unholy"

    def apply(self, target) -> None:
        target.max_hp = int(target.max_hp * 5)
        target.atk = int(target.atk * 2)
        target.crit_damage = target.crit_damage * 0.8
