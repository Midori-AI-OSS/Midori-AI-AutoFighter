from autofighter.effects import DamageOverTime


class Poison(DamageOverTime):
    plugin_type = "dot"
    id = "poison"

    def __init__(self, damage: int, turns: int) -> None:
        super().__init__("Poison", damage, turns, self.id)
