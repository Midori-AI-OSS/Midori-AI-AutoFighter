from dataclasses import dataclass


@dataclass
class Hostile:
    plugin_type = "themedadj"
    id = "hostile"
    name = "Hostile"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.05)
        target.defense = int(target.defense * 1.95)
