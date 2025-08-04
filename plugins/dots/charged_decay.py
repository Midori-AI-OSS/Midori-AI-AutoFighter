from autofighter.effects import DamageOverTime


class ChargedDecay(DamageOverTime):
    plugin_type = "dot"
    id = "charged_decay"

    def __init__(self, damage: int, turns: int) -> None:
        super().__init__("Charged Decay", damage, turns, self.id)

    def tick(self, target, *_):
        alive = super().tick(target)
        if not alive:
            target.stunned = True
        return alive
