from autofighter.effects import DamageOverTime


class FrozenWound(DamageOverTime):
    plugin_type = "dot"
    id = "frozen_wound"

    def __init__(self, damage: int, turns: int) -> None:
        super().__init__("Frozen Wound", damage, turns, self.id)

    def tick(self, target, *_):
        if target.actions_per_turn > 1:
            target.actions_per_turn -= 1
        return super().tick(target)
