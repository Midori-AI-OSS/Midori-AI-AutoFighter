from dataclasses import dataclass


@dataclass
class Disgusting:
    plugin_type = "themedadj"
    id = "disgusting"
    name = "Disgusting"

    def apply(self, target) -> None:
        target.defense = int(target.defense * 1.9)
