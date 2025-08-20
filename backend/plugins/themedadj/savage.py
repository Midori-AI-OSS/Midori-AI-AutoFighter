from dataclasses import dataclass


@dataclass
class Savage:
    plugin_type = "themedadj"
    id = "savage"
    name = "Savage"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.1)
        target.defense = int(target.defense * 1.9)
        target.max_hp = int(target.max_hp * 1.1)
