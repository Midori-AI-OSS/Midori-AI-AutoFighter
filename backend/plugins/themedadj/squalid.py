from dataclasses import dataclass


@dataclass
class Squalid:
    plugin_type = "themedadj"
    id = "squalid"
    name = "Squalid"

    def apply(self, target) -> None:
        target.defense = int(target.defense * 1.95)
        target.max_hp = int(target.max_hp * 1.05)
