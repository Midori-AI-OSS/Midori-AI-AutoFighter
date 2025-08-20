from dataclasses import dataclass


@dataclass
class Execrable:
    plugin_type = "themedadj"
    id = "execrable"
    name = "Execrable"

    def apply(self, target) -> None:
        target.max_hp = int(target.max_hp * 1.9)
