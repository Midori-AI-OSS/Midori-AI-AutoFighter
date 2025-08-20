from dataclasses import dataclass


@dataclass
class Spiteful:
    plugin_type = "themedadj"
    id = "spiteful"
    name = "Spiteful"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.07)
        target.max_hp = int(target.max_hp * 1.93)
