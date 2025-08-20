from dataclasses import dataclass


@dataclass
class Odious:
    plugin_type = "themedadj"
    id = "odious"
    name = "Odious"

    def apply(self, target) -> None:
        target.defense = int(target.defense * 1.95)
