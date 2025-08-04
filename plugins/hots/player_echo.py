from autofighter.effects import HealingOverTime


class PlayerEcho(HealingOverTime):
    plugin_type = "hot"
    id = "player_echo"

    def __init__(self, player_name: str, healing: int, turns: int) -> None:
        super().__init__(f"{player_name}'s Echo", healing, turns, self.id)

    def tick(self, target, damage=0, *_):
        target.apply_healing(int(damage * 0.2))
        self.turns -= 1
        return self.turns > 0
