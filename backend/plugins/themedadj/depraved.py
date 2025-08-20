from dataclasses import dataclass


@dataclass
class Depraved:
    plugin_type = "themedadj"
    id = "depraved"
    name = "Depraved"

    def apply(self, target) -> None:
        target.defense = int(target.defense - (target.defense * 0.1))
        target.atk = int(target.atk + (target.atk * 0.1))
