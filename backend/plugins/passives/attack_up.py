from dataclasses import dataclass


@dataclass
class AttackUp:
    plugin_type = "passive"
    id = "attack_up"
    name = "Attack Up"
    trigger = "battle_start"
    amount = 5

    def apply(self, target) -> None:
        target.atk += self.amount
