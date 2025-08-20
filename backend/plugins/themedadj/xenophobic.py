from dataclasses import dataclass


@dataclass
class Xenophobic:
    plugin_type = "themedadj"
    id = "xenophobic"
    name = "Xenophobic"

    def apply(self, target) -> None:
        target.defense = int(target.defense * 1.1)
