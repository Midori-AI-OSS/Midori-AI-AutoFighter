from autofighter.effects import HealingOverTime


class RadiantRegeneration(HealingOverTime):
    plugin_type = "hot"
    id = "radiant_regeneration"

    def __init__(self, healing: int = 5, turns: int = 2) -> None:
        super().__init__("Radiant Regeneration", healing, turns, self.id)
