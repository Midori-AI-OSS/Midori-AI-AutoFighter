from dataclasses import dataclass


@dataclass
class Ghoulish:
    plugin_type = "themedadj"
    id = "ghoulish"
    name = "Ghoulish"

    def apply(self, target) -> None:
        target.max_hp = int(target.max_hp * 1.95)
        target.atk = int(target.atk * 1.05)
