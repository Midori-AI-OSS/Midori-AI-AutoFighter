from autofighter.effects import DamageOverTime


class CelestialAtrophy(DamageOverTime):
    plugin_type = "dot"
    id = "celestial_atrophy"

    def __init__(self, damage: int, turns: int) -> None:
        super().__init__("Celestial Atrophy", damage, turns, self.id)

    def tick(self, target, *_):
        target.atk = max(target.atk - 1, 0)
        return super().tick(target)
