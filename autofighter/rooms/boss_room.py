from __future__ import annotations

from direct.gui.DirectGui import DGG
from panda3d.core import LColor

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
        )
        self.pattern = info.attacks
        self.reward = info.reward
        self.model_path = info.model
        self.music_path = info.music
        self._pattern_index = 0

    def setup(self) -> None:  # pragma: no cover - visual assets
        super().setup()
        if self.foe_model is not None:
            self.foe_model.setColor((0.5, 0, 0, 1))
        try:
            self.music = self.app.loader.loadSfx(self.music_path)
            self.music.setLoop(True)
            self.music.play()
        except Exception:
            self.music = None

    def foe_attack(self) -> None:
        assert self.attack_button is not None
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
        self.status_label["text"] = f"Boss hits! Player HP: {self.player.hp}/{self.player.max_hp}"
        if self.player.hp <= 0:
            self.attack_button["state"] = DGG.DISABLED
            self.status_label["text"] = "You were defeated!"
        else:
            self.attack_button["state"] = DGG.NORMAL
