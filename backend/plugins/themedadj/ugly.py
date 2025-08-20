from dataclasses import dataclass


@dataclass
class Ugly:
    plugin_type = "themedadj"
    id = "ugly"
    name = "Ugly"

    def apply(self, target) -> None:
        target.defense = int(target.defense * 1.1)
        target.max_hp = int(target.max_hp * 1.9)
