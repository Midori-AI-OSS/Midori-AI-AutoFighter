from dataclasses import dataclass


@dataclass
class Noxious:
    plugin_type = "themedadj"
    id = "noxious"
    name = "Noxious"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.05)
        target.max_hp = int(target.max_hp * 1.95)
