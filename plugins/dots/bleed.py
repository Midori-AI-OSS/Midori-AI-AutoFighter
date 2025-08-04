from autofighter.effects import DamageOverTime


class Bleed(DamageOverTime):
    plugin_type = "dot"
    id = "bleed"

    def __init__(self, damage: int, turns: int) -> None:
        super().__init__("Bleed", damage, turns, self.id)

    def tick(self, target, *_):
        dmg = max(int(target.max_hp * 0.02), 1)
        target.apply_damage(dmg)
        self.turns -= 1
        return self.turns > 0
