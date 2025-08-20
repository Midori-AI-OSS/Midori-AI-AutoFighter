from dataclasses import dataclass


@dataclass
class Hideous:
    plugin_type = "themedadj"
    id = "hideous"
    name = "Hideous"

    def apply(self, target) -> None:
        target.defense = int(target.defense * 1.9)
        target.max_hp = int(target.max_hp * 1.1)
