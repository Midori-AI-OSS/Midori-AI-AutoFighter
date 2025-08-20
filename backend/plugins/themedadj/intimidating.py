from dataclasses import dataclass


@dataclass
class Intimidating:
    plugin_type = "themedadj"
    id = "intimidating"
    name = "Intimidating"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.95)
        target.defense = int(target.defense * 1.05)
