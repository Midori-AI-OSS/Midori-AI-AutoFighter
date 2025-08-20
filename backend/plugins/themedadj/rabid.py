from dataclasses import dataclass


@dataclass
class Rabid:
    plugin_type = "themedadj"
    id = "rabid"
    name = "Rabid"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.1)
        target.defense = int(target.defense * 1.9)
