from autofighter.effects import HealingOverTime


class PlayerHeal(HealingOverTime):
    plugin_type = "hot"
    id = "player_heal"

    def __init__(self, player_name: str, healing: int, turns: int) -> None:
        super().__init__(f"{player_name}'s Heal", healing, turns, self.id)
        self.total_turns = turns

    def tick(self, target, *_):
        if self.turns == self.total_turns:
            target.apply_healing(self.healing)
        target.apply_healing(int(target.max_hp * 0.01))
        self.turns -= 1
        return self.turns > 0
