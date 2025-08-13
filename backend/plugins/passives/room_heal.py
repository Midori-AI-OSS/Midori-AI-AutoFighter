from dataclasses import dataclass


@dataclass
class RoomHeal:
    plugin_type = "passive"
    id = "room_heal"
    name = "Room Heal"
    trigger = "room_enter"
    amount = 1

    def apply(self, target) -> None:
        target.hp = min(target.hp + self.amount, target.max_hp)
