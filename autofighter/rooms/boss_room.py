from __future__ import annotations

from panda3d.core import LColor
from direct.gui.DirectGui import DGG

from autofighter.audio import get_audio
from autofighter.assets import AssetManager
from autofighter.battle_room import BattleRoom
from autofighter.rooms.boss_patterns import get_boss_info


class BossRoom(BattleRoom):
    """Battle scene with scripted boss attacks and rewards."""

    def __init__(
        self,
        app,
        return_scene_factory,
        *,
        boss_name: str = "demo",
        player=None,
        floor: int = 1,
        room: int = 1,
        pressure: int = 0,
        loop: int = 0,
        floor_boss: bool = False,
        assets: AssetManager | None = None,
    ) -> None:
        info = get_boss_info(boss_name)
        super().__init__(
            app,
            return_scene_factory,
            player=player,
            floor=floor,
            room=room,
            pressure=pressure,
            loop=loop,
            boss=not floor_boss,
            floor_boss=floor_boss,
            assets=assets,
        )
        self.pattern = info.attacks
        self.reward = info.reward
        self.foe_model_name = info.model
        self.music_name = info.music
        self._pattern_index = 0

    def setup(self) -> None:  # pragma: no cover - visual assets
        super().setup()
        if self.foe_model is not None:
            try:
                self.foe_model.setColor((0.5, 0, 0, 1))
            except Exception:
                pass
        try:
            get_audio().play_music(self.music_name)
        except Exception:
            pass

    def foe_attack(self) -> None:
        assert self.status_label is not None
        dmg = self.pattern[self._pattern_index]
        self._pattern_index = (self._pattern_index + 1) % len(self.pattern)
        self.turn += 1
        if self.turn >= self.overtime_threshold and not self.overtime:
            self.start_overtime()
        self.player.apply_damage(dmg)
        self.show_damage(self.player_model, dmg)
        self.show_attack_effect(self.foe_model, self.player_model, (1, 0, 0, 1))
        self.add_status_icon(self.player_model, LColor(0, 1, 0, 1))
        if self.player.hp <= 0:
            self.status_label["text"] = "You were defeated!"
        else:
            self.status_label["text"] = (
                f"Boss hits! Player HP: {self.player.hp}/{self.player.max_hp}"
            )
