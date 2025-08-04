from autofighter.effects import DamageOverTime


class BlazingTorment(DamageOverTime):
    plugin_type = "dot"
    id = "blazing_torment"

    def __init__(self, damage: int, turns: int) -> None:
        super().__init__("Blazing Torment", damage, turns, self.id)

    def on_action(self, target) -> None:
        super().tick(target)
