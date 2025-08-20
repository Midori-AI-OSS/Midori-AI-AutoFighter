from dataclasses import dataclass


@dataclass
class Filthy:
    plugin_type = "themedadj"
    id = "filthy"
    name = "Filthy"

    def apply(self, target) -> None:
        target.defense = int(target.defense * 1.95)
