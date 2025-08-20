from dataclasses import dataclass


@dataclass
class Threatening:
    plugin_type = "themedadj"
    id = "threatening"
    name = "Threatening"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.05)
        target.defense = int(target.defense * 1.95)
        target.dodge_odds = target.dodge_odds * 1.95
