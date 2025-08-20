from dataclasses import dataclass


@dataclass
class Fiendish:
    plugin_type = "themedadj"
    id = "fiendish"
    name = "Fiendish"

    def apply(self, target) -> None:
        target.dodge_odds = target.dodge_odds * 1.9
        target.crit_rate = target.crit_rate + 0.1
