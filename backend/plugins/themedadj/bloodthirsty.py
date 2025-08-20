from dataclasses import dataclass


@dataclass
class Bloodthirsty:
    plugin_type = "themedadj"
    id = "bloodthirsty"
    name = "Bloodthirsty"

    def apply(self, target) -> None:
        target.max_hp = int(target.max_hp - (target.max_hp * 0.1))
        target.atk = int(target.atk + (target.atk * 0.2))
