from dataclasses import dataclass


@dataclass
class Cannibalistic:
    plugin_type = "themedadj"
    id = "cannibalistic"
    name = "Cannibalistic"

    def apply(self, target) -> None:
        target.max_hp = int(target.max_hp + (target.max_hp * 0.05))
