from dataclasses import dataclass


@dataclass
class Primitive:
    plugin_type = "themedadj"
    id = "primitive"
    name = "Primitive"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.05)
        target.defense = int(target.defense * 1.95)
