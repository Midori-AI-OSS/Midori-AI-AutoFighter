from __future__ import annotations

try:
    from direct.gui import DirectGuiGlobals as DGG
    from direct.gui.DirectGui import DirectFrame
    from direct.gui.DirectGui import DirectLabel
    from direct.gui.DirectGui import DirectButton
    from direct.gui.DirectGui import DirectSlider
    from direct.gui.DirectGui import DirectCheckButton
    from direct.showbase.ShowBase import ShowBase
except Exception:  # pragma: no cover - fallback for headless tests
    class _Widget:
        """Minimal widget stand-ins for headless tests."""

        def __init__(self, **kwargs: object) -> None:
            self.options = dict(kwargs)

        def __getitem__(self, key: str) -> object:
            return self.options.get(key)

        def __setitem__(self, key: str, value: object) -> None:
            self.options[key] = value

        def destroy(self) -> None:  # noqa: D401 - match Panda3D API
            """Pretend to remove the widget."""

        def bind(self, *_args: object, **_kwargs: object) -> None:
            pass

        def unbind(self, *_args: object, **_kwargs: object) -> None:
            pass

    class DirectButton(_Widget):  # type: ignore[dead-code]
        pass

    class DirectCheckButton(_Widget):  # type: ignore[dead-code]
        def setIndicatorValue(self, value: bool, *_args: object, **_kwargs: object) -> None:
            self.options["indicatorValue"] = value

    class DirectFrame(_Widget):  # type: ignore[dead-code]
        pass

    class DirectLabel(_Widget):  # type: ignore[dead-code]
        pass

    class DirectSlider(_Widget):  # type: ignore[dead-code]
        def command(self) -> None:  # pragma: no cover - optional callback
            func = self.options.get("command")
            if callable(func):
                func()

    class ShowBase:  # type: ignore[dead-code]
        pass

from autofighter.gui import FRAME_COLOR
from autofighter.gui import TEXT_COLOR
from autofighter.gui import get_slider_scale
from autofighter.gui import get_widget_scale
from autofighter.gui import set_widget_pos
from autofighter.assets import get_texture
from autofighter.audio import get_audio
from autofighter.save import save_settings
from autofighter.scene import Scene


def add_tooltip(widget: DirectFrame | DirectButton | DirectSlider | DirectCheckButton, text: str) -> None:
    try:
        tooltip = DirectLabel(
            text=text,
            text_fg=TEXT_COLOR,
            frameColor=FRAME_COLOR,
            scale=get_widget_scale(),
            parent=widget,
            pos=(0, 0, -0.2),
        )
        tooltip.hide()
        widget.bind(DGG.ENTER, lambda *_: tooltip.show())
        widget.bind(DGG.EXIT, lambda *_: tooltip.hide())
    except Exception:  # pragma: no cover - headless tests
        pass


class OptionsMenu(Scene):
    def __init__(self, app: ShowBase) -> None:
        self.app = app
        self.widgets: list[DirectButton | DirectCheckButton | DirectSlider] = []
        self.index = 0
        audio_mgr = get_audio()
        self.sfx_volume = audio_mgr.sfx_volume
        self.music_volume = audio_mgr.music_volume
        self.stat_refresh_rate = getattr(self.app, "stat_refresh_rate", 5)
        self.pause_on_stats = getattr(self.app, "pause_on_stats", True)

    BUTTON_SPACING = 0.3
    def setup(self) -> None:
        self.sfx_slider = DirectSlider(
            range=(0, 1),
            value=self.sfx_volume,
            scale=get_slider_scale(),
            frameColor=FRAME_COLOR,
            command=self.update_sfx,
        )
        DirectFrame(
            parent=self.sfx_slider,
            image=get_texture("icon_volume_2"),
            frameColor=(0, 0, 0, 0),
            scale=get_widget_scale(),
            pos=(-0.7, 0, 0),
        )
        DirectLabel(
            parent=self.sfx_slider,
            text="SFX Volume",
            text_fg=TEXT_COLOR,
            frameColor=(0, 0, 0, 0),
            scale=get_widget_scale(),
            pos=(-0.3, 0, 0),
        )
        add_tooltip(self.sfx_slider, "Adjust sound effect volume.")

        self.music_slider = DirectSlider(
            range=(0, 1),
            value=self.music_volume,
            scale=get_slider_scale(),
            frameColor=FRAME_COLOR,
            command=self.update_music,
        )
        DirectFrame(
            parent=self.music_slider,
            image=get_texture("icon_music"),
            frameColor=(0, 0, 0, 0),
            scale=get_widget_scale(),
            pos=(-0.7, 0, 0),
        )
        DirectLabel(
            parent=self.music_slider,
            text="Music Volume",
            text_fg=TEXT_COLOR,
            frameColor=(0, 0, 0, 0),
            scale=get_widget_scale(),
            pos=(-0.3, 0, 0),
        )
        add_tooltip(self.music_slider, "Adjust background music volume.")

        self.refresh_slider = DirectSlider(
            range=(1, 10),
            value=self.stat_refresh_rate,
            scale=get_slider_scale(),
            frameColor=FRAME_COLOR,
            command=self.update_refresh,
        )
        DirectFrame(
            parent=self.refresh_slider,
            image=get_texture("icon_refresh_cw"),
            frameColor=(0, 0, 0, 0),
            scale=get_widget_scale(),
            pos=(-0.7, 0, 0),
        )
        DirectLabel(
            parent=self.refresh_slider,
            text="Refresh Rate",
            text_fg=TEXT_COLOR,
            frameColor=(0, 0, 0, 0),
            scale=get_widget_scale(),
            pos=(-0.3, 0, 0),
        )
        add_tooltip(self.refresh_slider, "Update stats every N frames.")

        self._pause_button = DirectCheckButton(
            text="Pause on Stat Screen",
            frameColor=FRAME_COLOR,
            text_fg=TEXT_COLOR,
            indicatorValue=self.pause_on_stats,
            command=self.toggle_pause,
            scale=get_widget_scale(),
        )
        DirectFrame(
            parent=self._pause_button,
            image=get_texture("icon_pause"),
            frameColor=(0, 0, 0, 0),
            scale=get_widget_scale(),
            pos=(-1.2, 0, 0),
        )
        add_tooltip(self._pause_button, "Stop gameplay while viewing stats.")

        self._back_button = DirectButton(
            text="Back",
            frameColor=FRAME_COLOR,
            text_fg=TEXT_COLOR,
            command=self.back,
            scale=get_widget_scale(),
        )
        add_tooltip(self._back_button, "Return to main menu.")
        self.widgets = [
            self.sfx_slider,
            self.music_slider,
            self.refresh_slider,
            self._pause_button,
            self._back_button,
        ]
        top = self.BUTTON_SPACING * (len(self.widgets) - 1) / 2
        for i, widget in enumerate(self.widgets):
            set_widget_pos(widget, (0, 0, top - i * self.BUTTON_SPACING))
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
            color = (0.2, 0.2, 0.2, 0.9) if i == self.index else FRAME_COLOR
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
            min_val, max_val = widget["range"]
            step = 0.05 if max_val <= 1 else 1
            widget["value"] = max(min_val, widget["value"] - step)
            widget.command()

    def increase(self) -> None:
        widget = self.widgets[self.index]
        if isinstance(widget, DirectSlider):
            min_val, max_val = widget["range"]
            step = 0.05 if max_val <= 1 else 1
            widget["value"] = min(max_val, widget["value"] + step)
            widget.command()

    def update_sfx(self) -> None:
        self.sfx_volume = float(self.sfx_slider["value"])
        get_audio().set_sfx_volume(self.sfx_volume)
        save_settings(self._settings_payload())

    def update_music(self) -> None:
        self.music_volume = float(self.music_slider["value"])
        get_audio().set_music_volume(self.music_volume)
        save_settings(self._settings_payload())

    def update_refresh(self) -> None:
        self.stat_refresh_rate = int(self.refresh_slider["value"])
        self.app.stat_refresh_rate = self.stat_refresh_rate
        save_settings(self._settings_payload())

    def toggle_pause(self, _=None) -> None:
        self.pause_on_stats = bool(self.pause_button["indicatorValue"])
        self.app.pause_on_stats = self.pause_on_stats
        save_settings(self._settings_payload())

    def back(self) -> None:
        from autofighter.menu import MainMenu  # local import to avoid circular dependency

        self.app.scene_manager.switch_to(MainMenu(self.app))

    @property
    def pause_button(self) -> DirectCheckButton:
        return self._pause_button

    @property
    def back_button(self) -> DirectButton:
        return self._back_button

    def _settings_payload(self) -> dict[str, object]:
        return {
            "sfx_volume": self.sfx_volume,
            "music_volume": self.music_volume,
            "stat_refresh_rate": self.stat_refresh_rate,
            "pause_on_stats": self.pause_on_stats,
        }
