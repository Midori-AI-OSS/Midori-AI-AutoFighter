from dataclasses import dataclass


@dataclass
class Beastly:
    plugin_type = "themedadj"
    id = "beastly"
    name = "Beastly"

    def apply(self, target) -> None:
        target.max_hp = int(target.max_hp * 1.05)
        target.atk = int(target.atk * 1.05)
