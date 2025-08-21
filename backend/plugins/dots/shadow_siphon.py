from autofighter.effects import DamageOverTime


class ShadowSiphon(DamageOverTime):
    plugin_type = "dot"
    id = "shadow_siphon"

    def __init__(self, damage: int) -> None:
        super().__init__("Shadow Siphon", damage, 1, self.id)

    async def tick(self, target, *_):
        await super().tick(target)
        self.turns += 1
        return True
