from autofighter.effects import DamageOverTime


class AbyssalWeakness(DamageOverTime):
    plugin_type = "dot"
    id = "abyssal_weakness"

    def __init__(self, damage: int, turns: int) -> None:
        super().__init__("Abyssal Weakness", damage, turns, self.id)
        self._applied = False

    def tick(self, target, *_):
        if not self._applied:
            target.defense = max(target.defense - 1, 0)
            self._applied = True
        alive = super().tick(target)
        if not alive:
            target.defense += 1
        return alive
