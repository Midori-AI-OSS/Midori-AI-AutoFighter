from __future__ import annotations

import random

from direct.task import Task
from panda3d.core import LColor
from panda3d.core import LVector3f
from panda3d.core import NodePath
from direct.gui.DirectGui import DGG
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectLabel
from direct.showbase.ShowBase import ShowBase

from autofighter.gui import set_widget_pos
from autofighter.scene import Scene
from autofighter.stats import Stats
from autofighter.rewards import Reward
from autofighter.rewards import select_rewards


class BattleRoom(Scene):
    """Turn-based combat scene with basic effects and scaling."""

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
        boss: bool = False,
        floor_boss: bool = False,
    ) -> None:
        self.app = app
        self.return_scene_factory = return_scene_factory
        self.player = player or Stats(hp=100, max_hp=100, atk=10, defense=5)
        self.base_foe = Stats(hp=50, max_hp=50, atk=5, defense=3)
        self.foe = self.scale_foe(floor, room, pressure, loop)
        self.pressure = pressure
        self.loop = loop
        self.boss = boss
        self.floor_boss = floor_boss
        self.turn = 0
        self.overtime_threshold = 500 if floor_boss else 100
        self.overtime = False
        self.widgets: list[DirectButton | DirectLabel] = []
        self.overtime_label: DirectLabel | None = None
        self.enraged_icon: DirectLabel | None = None
        self.player_model: NodePath | None = None
        self.foe_model: NodePath | None = None
        self.attack_button: DirectButton | None = None
        self.status_label: DirectLabel | None = None
        self.status_icons: list[NodePath] = []
        self._flash_task: Task | None = None
        self._flash_state = False
        self.reward: Reward | None = None

    def setup(self) -> None:
        self.player_model = self.app.loader.loadModel("models/box")
        self.player_model.reparentTo(self.app.render)
        self.player_model.setPos(-1, 10, 0)

        self.foe_model = self.app.loader.loadModel("models/box")
        self.foe_model.reparentTo(self.app.render)
        self.foe_model.setPos(1, 10, 0)

        self.attack_button = DirectButton(
            text="Attack",
            command=self.send_player_attack,
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(self.attack_button, (0, 0, -0.7))
        self.status_label = DirectLabel(
            text="A wild foe appears!",
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(self.status_label, (0, 0, 0.7))
        self.overtime_label = DirectLabel(
            text="Overtime! Foes grow enraged.",
            frameColor=(0.5, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
            relief=None,
        )
        set_widget_pos(self.overtime_label, (0, 0, 0.5))
        self.overtime_label.hide()
        self.widgets = [self.attack_button, self.status_label, self.overtime_label]
        self.app.accept("escape", self.exit)
        self.app.accept("player-attack", self.player_attack)
        self.app.accept("foe-attack", self.foe_attack)

    def teardown(self) -> None:
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        if self.player_model is not None:
            self.player_model.removeNode()
        if self.foe_model is not None:
            self.foe_model.removeNode()
        for icon in self.status_icons:
            icon.removeNode()
        self.status_icons.clear()
        if self._flash_task is not None:
            self.app.taskMgr.remove(self._flash_task)
            self._flash_task = None
            self.app.setBackgroundColor(LColor(0, 0, 0, 1))
        self.app.ignore("escape")
        self.app.ignore("player-attack")
        self.app.ignore("foe-attack")

    def scale_foe(
        self, floor: int, room: int, pressure: int, loop: int
    ) -> Stats:
        factor = floor * room * (1 + 0.05 * pressure) * (1.2 ** loop)
        return Stats(
            hp=int(self.base_foe.hp * factor),
            max_hp=int(self.base_foe.max_hp * factor),
            atk=int(self.base_foe.atk * factor),
            defense=int(self.base_foe.defense * factor),
        )

    def send_player_attack(self) -> None:
        self.app.messenger.send("player-attack")

    def player_attack(self) -> None:
        assert self.attack_button is not None
        assert self.status_label is not None
        self.attack_button["state"] = DGG.DISABLED
        hit_chance = self.player.atk / (self.player.atk + self.foe.defense)
        if random.random() < hit_chance:
            dmg = self.player.atk
            self.foe.apply_damage(dmg)
            self.show_damage(self.foe_model, dmg)
            self.show_attack_effect(self.player_model, self.foe_model, (1, 1, 0, 1))
            self.add_status_icon(self.foe_model, LColor(1, 0, 0, 1))
            text = f"Hit! Foe HP: {self.foe.hp}/{self.foe.max_hp}"
        else:
            text = "Miss!"
        if self.foe.hp <= 0:
            self.reward = select_rewards(
                boss=self.boss,
                floor_boss=self.floor_boss,
                loop=self.loop,
                pressure=self.pressure,
            )
            parts = [
                f"Gold {self.reward.gold}",
                f"Card {self.reward.card}★",
                f"Upgrade {self.reward.upgrade}★",
            ]
            if self.reward.relic is not None:
                parts.append(f"Relic {self.reward.relic}★")
            if self.reward.tickets:
                parts.append(f"Tickets {self.reward.tickets}")
            reward_text = ", ".join(parts)
            self.status_label["text"] = f"Foe defeated! {reward_text}"
            self.attack_button["state"] = DGG.DISABLED
        else:
            self.status_label["text"] = text
            self.app.messenger.send("foe-attack")

    def foe_attack(self) -> None:
        assert self.attack_button is not None
        assert self.status_label is not None
        self.turn += 1
        if self.turn >= self.overtime_threshold and not self.overtime:
            self.start_overtime()
        hit_chance = self.foe.atk / (self.foe.atk + self.player.defense)
        if random.random() < hit_chance:
            dmg = self.foe.atk
            self.player.apply_damage(dmg)
            self.show_damage(self.player_model, dmg)
            self.show_attack_effect(self.foe_model, self.player_model, (1, 0, 0, 1))
            self.add_status_icon(self.player_model, LColor(0, 1, 0, 1))
            text = f"Foe hits! Player HP: {self.player.hp}/{self.player.max_hp}"
        else:
            text = "Foe misses!"
        self.status_label["text"] = text
        if self.player.hp <= 0:
            self.attack_button["state"] = DGG.DISABLED
            self.status_label["text"] = "You were defeated!"
        else:
            self.attack_button["state"] = DGG.NORMAL

    def show_damage(self, target: NodePath | None, amount: int) -> None:
        pos = (-0.7, 0, 0.2)
        if target is self.foe_model:
            pos = (0.7, 0, 0.2)
        label = DirectLabel(
            text=str(amount),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 0, 0, 1),
        )
        set_widget_pos(label, pos)
        self.widgets.append(label)
        self.flash_model(target)
        self.app.taskMgr.doMethodLater(
            0.5, self._remove_widget, "remove-dmg", extraArgs=[label], appendTask=True
        )

    def show_attack_effect(
        self, source: NodePath | None, target: NodePath | None, color: tuple[float, float, float, float]
    ) -> None:
        if source is None or target is None:
            return
        effect = self.app.loader.loadModel("models/box")
        effect.reparentTo(self.app.render)
        effect.setScale(0.2)
        effect.setColor(color)
        start = LVector3f(source.getPos())
        end = LVector3f(target.getPos())
        mid = (start + end) * 0.5
        effect.setPos(mid)
        self.app.taskMgr.doMethodLater(
            0.3, self._remove_effect, "remove-effect", extraArgs=[effect], appendTask=True
        )

    def _remove_effect(self, effect: NodePath, task: Task) -> Task:
        effect.removeNode()
        return Task.done

    def _remove_widget(self, widget: DirectLabel, task: Task) -> Task:
        widget.destroy()
        return Task.done

    def flash_model(self, model: NodePath | None) -> None:
        if model is None:
            return
        model.setColor(LColor(1, 0, 0, 1))
        self.app.taskMgr.doMethodLater(
            0.2,
            lambda task: model.setColor(LColor(1, 1, 1, 1)) or Task.done,
            "flash-reset",
        )

    def add_status_icon(self, target: NodePath | None, color: LColor) -> None:
        if target is None:
            return
        icon = self.app.loader.loadModel("models/box")
        icon.reparentTo(target)
        icon.setScale(0.2)
        icon.setColor(color)
        icon.setPos(0, 0, 1)
        self.status_icons.append(icon)

    def start_overtime(self) -> None:
        assert self.overtime_label is not None
        self.overtime = True
        self.overtime_label.show()
        if self.enraged_icon is None:
            self.enraged_icon = DirectLabel(
                text="Enraged",
                frameColor=(0, 0, 0, 0),
                text_fg=(1, 0, 0, 1),
            )
            set_widget_pos(self.enraged_icon, (0.7, 0, 0.4))
            self.widgets.append(self.enraged_icon)
            self.foe.atk = int(self.foe.atk * 1.4)
        if self._flash_task is None:
            self._flash_task = self.app.taskMgr.doMethodLater(
                0.5, self._overtime_flash, "overtime-flash", appendTask=True
            )

    def _overtime_flash(self, task: Task) -> Task:
        self._flash_state = not self._flash_state
        color = LColor(1, 0, 0, 1) if self._flash_state else LColor(0, 0, 1, 1)
        self.app.setBackgroundColor(color)
        return task.again

    def exit(self) -> None:
        self.app.scene_manager.switch_to(self.return_scene_factory())
