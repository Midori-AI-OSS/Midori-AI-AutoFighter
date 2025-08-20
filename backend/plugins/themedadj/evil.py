from dataclasses import dataclass


@dataclass
class Evil:
    plugin_type = "themedadj"
    id = "evil"
    name = "Evil"

    def apply(self, target) -> None:
        target.max_hp = int(target.max_hp * 1.95)
        target.atk = int(target.atk * 1.05)
