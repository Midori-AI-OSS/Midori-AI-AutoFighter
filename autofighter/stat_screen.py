from __future__ import annotations

from typing import Callable

try:
    from panda3d.core import TextNode
    from direct.gui.DirectFrame import DirectFrame
    from direct.gui.OnscreenText import OnscreenText
    from direct.showbase.ShowBase import ShowBase
except Exception:  # pragma: no cover - fallback for headless tests
    class TextNode:
        A_left = 0

    class DirectFrame:  # type: ignore[dead-code]
        def __init__(self, **_kwargs: object) -> None:
            pass

        def destroy(self) -> None:
            pass

    class OnscreenText:  # type: ignore[dead-code]
        def __init__(self, text: str, **_kwargs: object) -> None:
            self.text = text

        def destroy(self) -> None:
            pass

    class ShowBase:  # type: ignore[dead-code]
        pass

from autofighter.scene import Scene
from autofighter.stats import Stats


class StatScreen(Scene):
    """Display player statistics and status effects."""

    def __init__(
        self,
        app: ShowBase,
        stats: Stats,
        *,
        refresh_rate: int | None = None,
        return_scene_factory: Callable[[], Scene] | None = None,
    ) -> None:
        self.app = app
        self.stats = stats
        rate = refresh_rate if refresh_rate is not None else getattr(app, "stat_refresh_rate", 5)
        self.refresh_rate = max(1, min(int(rate), 10))
        self.return_scene_factory = return_scene_factory
        self.frame: DirectFrame | None = None
        self.lines: list[OnscreenText] = []
        self.tick_count = 0
        self.status_hooks: list[Callable[[Stats], list[str]]] = []
        self.was_paused = False

    def setup(self) -> None:
        if getattr(self.app, "pause_on_stats", False):
            self.app.pause_game()
            self.was_paused = True
        self.frame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.app.accept("escape", self.close)
        self.app.taskMgr.add(self._update_task, "stat-screen-update")
        self._render()

    def teardown(self) -> None:
        if self.frame:
            self.frame.destroy()
            self.frame = None
        for line in self.lines:
            line.destroy()
        self.lines.clear()
        self.app.taskMgr.remove("stat-screen-update")
        self.app.ignore("escape")
        if self.was_paused:
            self.app.resume_game()

    def _update_task(self, task):
        self.tick_count = (self.tick_count + 1) % self.refresh_rate
        if self.tick_count == 0:
            self._render()
        return task.cont

    def _render(self) -> None:
        for line in self.lines:
            line.destroy()
        self.lines.clear()

        entries: list[str] = []
        entries.append("Core:")
        entries.append(f" HP: {self.stats.hp}/{self.stats.max_hp}")
        entries.append(f" EXP: {self.stats.exp}")
        entries.append(f" Level: {self.stats.level}")
        entries.append(f" EXP Multiplier: {self.stats.exp_multiplier}")
        entries.append(f" Actions/Turn: {self.stats.actions_per_turn}")

        entries.append("Offense:")
        entries.append(f" Attack: {self.stats.atk}")
        entries.append(f" Crit Rate: {self.stats.crit_rate}")
        entries.append(f" Crit Damage: {self.stats.crit_damage}")
        entries.append(f" Effect Hit Rate: {self.stats.effect_hit_rate}")
        entries.append(f" Base Damage Type: {self.stats.base_damage_type}")

        entries.append("Defense:")
        entries.append(f" Defense: {self.stats.defense}")
        entries.append(f" Mitigation: {self.stats.mitigation}")
        entries.append(f" Regain: {self.stats.regain}")
        entries.append(f" Dodge Odds: {self.stats.dodge_odds}")
        entries.append(f" Effect Resistance: {self.stats.effect_resistance}")

        entries.append("Vitality & Advanced:")
        entries.append(f" Vitality: {self.stats.vitality}")
        entries.append(f" Action Points: {self.stats.action_points}")
        entries.append(f" Damage Taken: {self.stats.damage_taken}")
        entries.append(f" Damage Dealt: {self.stats.damage_dealt}")
        entries.append(f" Kills: {self.stats.kills}")

        entries.append("Status:")
        entries.append(
            " Passives: " + (", ".join(self.stats.passives) or "None")
        )
        entries.append(" DoTs: " + (", ".join(self.stats.dots) or "None"))
        entries.append(" HoTs: " + (", ".join(self.stats.hots) or "None"))
        entries.append(
            " Damage Types: " + (", ".join(self.stats.damage_types) or "None")
        )
        entries.append(" Relics: " + (", ".join(self.stats.relics) or "None"))

        for hook in self.status_hooks:
            entries.extend(hook(self.stats))

        for i, text in enumerate(entries):
            item = OnscreenText(
                text=text,
                pos=(-1.2, 0.9 - i * 0.07),
                align=TextNode.A_left,
                scale=0.05,
            )
            self.lines.append(item)

    def add_status_hook(self, hook: Callable[[Stats], list[str]]) -> None:
        self.status_hooks.append(hook)

    def close(self) -> None:
        scene = self.return_scene_factory() if self.return_scene_factory else None
        self.app.scene_manager.switch_to(scene)
