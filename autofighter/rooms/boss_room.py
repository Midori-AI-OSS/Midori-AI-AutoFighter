from __future__ import annotations

from direct.showbase.ShowBase import ShowBase

from autofighter.stats import Stats
from autofighter.battle_room import BattleRoom


class BossRoom(BattleRoom):
    """Standard boss fight that concludes a floor."""

    def __init__(
        self,
        app: ShowBase,
        return_scene_factory,
        player: Stats | None = None,
        *,
        floor: int = 1,
        room: int = 1,
        pressure: int = 0,
        loop: int = 0,
    ) -> None:
        super().__init__(
            app,
            return_scene_factory,
            player,
            floor=floor,
            room=room,
            pressure=pressure,
            loop=loop,
            floor_boss=False,
        )
