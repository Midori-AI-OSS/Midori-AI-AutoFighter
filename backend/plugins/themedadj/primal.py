from dataclasses import dataclass


@dataclass
class Primal:
    plugin_type = "themedadj"
    id = "primal"
    name = "Primal"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.05)
        target.defense = int(target.defense * 1.95)
        target.max_hp = int(target.max_hp * 1.05)
