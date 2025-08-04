from __future__ import annotations

from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectCheckButton
from direct.gui.DirectGui import DirectSlider
from direct.showbase.ShowBase import ShowBase

from autofighter.save import load_player
from autofighter.scene import Scene
from autofighter.battle_room import BattleRoom
from autofighter.player_creator import PlayerCreator


class MainMenu(Scene):
    def __init__(self, app: ShowBase) -> None:
        self.app = app
        self.buttons: list[DirectButton] = []
        self.index = 0

    def setup(self) -> None:
        labels = [
            ("New Run", self.new_run),
            ("Load Run", self.load_run),
            ("Edit Player", self.edit_player),
            ("Options", self.open_options),
            ("Quit", self.app.userExit),
        ]
        for i, (text, cmd) in enumerate(labels):
            button = DirectButton(
                text=text,
                command=cmd,
                pos=(0, 0, 0.4 - i * 0.2),
                frameColor=(0, 0, 0, 0.5),
                text_fg=(1, 1, 1, 1),
            )
            self.buttons.append(button)
        self.highlight()
        self.app.accept("arrow_up", self.prev)
        self.app.accept("arrow_down", self.next)
        self.app.accept("enter", self.activate)

    def teardown(self) -> None:
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()
        self.app.ignore("arrow_up")
        self.app.ignore("arrow_down")
        self.app.ignore("enter")

    def highlight(self) -> None:
        for i, button in enumerate(self.buttons):
            color = (0.2, 0.2, 0.2, 0.9) if i == self.index else (0, 0, 0, 0.5)
            button["frameColor"] = color

    def prev(self) -> None:
        self.index = (self.index - 1) % len(self.buttons)
        self.highlight()

    def next(self) -> None:
        self.index = (self.index + 1) % len(self.buttons)
        self.highlight()

    def activate(self) -> None:
        self.buttons[self.index]["command"]()

    def new_run(self) -> None:
        loaded = load_player()
        if not loaded:
            print("No saved player. Use Edit Player first.")
            return
        _, _, _, _, stats = loaded
        battle = BattleRoom(self.app, return_scene_factory=lambda: MainMenu(self.app), player=stats)
        self.app.scene_manager.switch_to(battle)

    def load_run(self) -> None:  # stub
        print("Load Run")

    def edit_player(self) -> None:
        creator = PlayerCreator(
            self.app,
            return_scene_factory=lambda: MainMenu(self.app),
        )
        self.app.scene_manager.switch_to(creator)

    def open_options(self) -> None:
        self.app.scene_manager.switch_to(OptionsMenu(self.app))


class OptionsMenu(Scene):
    def __init__(self, app: ShowBase) -> None:
        self.app = app
        self.widgets: list[DirectButton | DirectCheckButton | DirectSlider] = []
        self.index = 0
        self.sfx_volume = 0.5
        self.music_volume = 0.5
        self.pause_on_stats = getattr(self.app, "pause_on_stats", True)

    def setup(self) -> None:
        sfx = DirectSlider(
            range=(0, 1),
            value=self.sfx_volume,
            pos=(0, 0, 0.3),
            scale=0.5,
            frameColor=(0, 0, 0, 0.5),
            command=self.update_sfx,
        )
        music = DirectSlider(
            range=(0, 1),
            value=self.music_volume,
            pos=(0, 0, 0.0),
            scale=0.5,
            frameColor=(0, 0, 0, 0.5),
            command=self.update_music,
        )
        pause = DirectCheckButton(
            text="Pause on Stat Screen",
            pos=(0, 0, -0.3),
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
            indicatorValue=self.pause_on_stats,
            command=self.toggle_pause,
        )
        back = DirectButton(
            text="Back",
            pos=(0, 0, -0.6),
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
            command=self.back,
        )
        self.widgets = [sfx, music, pause, back]
        self.highlight()
        self.app.accept("arrow_up", self.prev)
        self.app.accept("arrow_down", self.next)
        self.app.accept("arrow_left", self.decrease)
        self.app.accept("arrow_right", self.increase)
        self.app.accept("enter", self.activate)
        self.app.accept("escape", self.back)

    def teardown(self) -> None:
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        self.app.ignore("arrow_up")
        self.app.ignore("arrow_down")
        self.app.ignore("arrow_left")
        self.app.ignore("arrow_right")
        self.app.ignore("enter")
        self.app.ignore("escape")

    def highlight(self) -> None:
        for i, widget in enumerate(self.widgets):
            color = (0.2, 0.2, 0.2, 0.9) if i == self.index else (0, 0, 0, 0.5)
            widget["frameColor"] = color

    def prev(self) -> None:
        self.index = (self.index - 1) % len(self.widgets)
        self.highlight()

    def next(self) -> None:
        self.index = (self.index + 1) % len(self.widgets)
        self.highlight()

    def activate(self) -> None:
        widget = self.widgets[self.index]
        if widget == self.back_button:
            self.back()
        elif widget == self.pause_button:
            self.pause_button.setIndicatorValue(not self.pause_button["indicatorValue"])
            self.toggle_pause()

    def decrease(self) -> None:
        widget = self.widgets[self.index]
        if isinstance(widget, DirectSlider):
            widget["value"] = max(widget["range"][0], widget["value"] - 0.05)
            widget.command()

    def increase(self) -> None:
        widget = self.widgets[self.index]
        if isinstance(widget, DirectSlider):
            widget["value"] = min(widget["range"][1], widget["value"] + 0.05)
            widget.command()

    def update_sfx(self) -> None:
        self.sfx_volume = self.widgets[0]["value"]

    def update_music(self) -> None:
        self.music_volume = self.widgets[1]["value"]

    def toggle_pause(self, _=None) -> None:
        self.pause_on_stats = bool(self.widgets[2]["indicatorValue"])
        self.app.pause_on_stats = self.pause_on_stats

    def back(self) -> None:
        self.app.scene_manager.switch_to(MainMenu(self.app))

    @property
    def pause_button(self) -> DirectCheckButton:
        return self.widgets[2]  # type: ignore[return-value]

    @property
    def back_button(self) -> DirectButton:
        return self.widgets[3]  # type: ignore[return-value]
