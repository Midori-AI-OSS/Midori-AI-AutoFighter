from dataclasses import dataclass


@dataclass
class Insidious:
    plugin_type = "themedadj"
    id = "insidious"
    name = "Insidious"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.05)
        target.dodge_odds = target.dodge_odds * 1.05
