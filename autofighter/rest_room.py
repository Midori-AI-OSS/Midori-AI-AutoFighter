from __future__ import annotations

try:
    from direct.gui.DirectGui import DirectLabel
    from direct.gui.DirectGui import DirectButton
    from direct.showbase.ShowBase import ShowBase
    from direct.interval.IntervalGlobal import Func
    from direct.interval.IntervalGlobal import Wait
    from direct.interval.IntervalGlobal import Sequence
except Exception:  # pragma: no cover - headless tests
    class _Widget:
        def __init__(self, **kwargs: object) -> None:
            self.options = dict(kwargs)

        def __getitem__(self, key: str) -> object:
            return self.options.get(key)

        def __setitem__(self, key: str, value: object) -> None:
            self.options[key] = value

        def destroy(self) -> None:
            pass

    class DirectLabel(_Widget):  # type: ignore[dead-code]
        def setText(self, text: str) -> None:
            self.options["text"] = text

    class DirectButton(_Widget):  # type: ignore[dead-code]
        pass

    class ShowBase:  # type: ignore[dead-code]
        pass

    def Func(func, *args: object, **kwargs: object):  # type: ignore[dead-code]
        return lambda: func(*args, **kwargs)

    def Wait(_duration: float):  # type: ignore[dead-code]
        return lambda: None

    class Sequence:  # type: ignore[dead-code]
        def __init__(self, *actions: object) -> None:
            self.actions = actions

        def start(self) -> None:
            for action in self.actions:
                if callable(action):
                    action()

from autofighter.gui import set_widget_pos
from autofighter.scene import Scene
from autofighter.stats import Stats


class RestRoom(Scene):
    """Scene offering healing or item trades with limited uses."""

    uses_per_floor: dict[int, int] = {}
    max_uses_per_floor: int = 1
    min_rests_per_floor: int = 2

    def __init__(
        self,
        app: ShowBase,
        stats: Stats,
        return_scene_factory,
        *,
        floor: int = 1,
        items: dict[str, int] | None = None,
    ) -> None:
        self.app = app
        self.stats = stats
        self.return_scene_factory = return_scene_factory
        self.floor = floor
        self.items = items or {"Upgrade Stone": 0}
        self.widgets: list[DirectButton | DirectLabel] = []
        self.heal_button: DirectButton | None = None
        self.trade_button: DirectButton | None = None
        self.info_label: DirectLabel | None = None

    def setup(self) -> None:
        self.info_label = DirectLabel(
            text=self._info_text(),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(self.info_label, (0, 0, 0.7))
        self.heal_button = DirectButton(
            text="Heal",
            command=self.heal,
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(self.heal_button, (-0.3, 0, -0.7))
        self.trade_button = DirectButton(
            text="Trade",
            command=self.trade,
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(self.trade_button, (0.3, 0, -0.7))
        leave_button = DirectButton(
            text="Leave",
            command=self.exit,
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(leave_button, (0, 0, -0.9))
        self.widgets = [
            self.info_label,
            self.heal_button,
            self.trade_button,
            leave_button,
        ]
        self._check_uses()
        self.app.accept("escape", self.exit)

    def teardown(self) -> None:
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        self.app.ignore("escape")

    def heal(self) -> None:
        if self._uses_left() <= 0:
            return
        self.stats.hp = self.stats.max_hp
        self._record_use()
        self._animate("Healed to full!")

    def trade(self) -> None:
        if self._uses_left() <= 0:
            return
        if self.items.get("Upgrade Stone", 0) <= 0:
            return
        self.items["Upgrade Stone"] -= 1
        self.stats.max_hp += 5
        self.stats.hp = self.stats.max_hp
        self._record_use()
        self._animate("Traded stone for +5 Max HP")

    def _update(self) -> None:
        assert self.info_label is not None
        self.info_label["text"] = self._info_text()
        self._check_uses()

    def _check_uses(self) -> None:
        if self._uses_left() <= 0:
            if self.heal_button is not None:
                self.heal_button["state"] = "disabled"
            if self.trade_button is not None:
                self.trade_button["state"] = "disabled"

    def _info_text(self) -> str:
        stones = self.items.get("Upgrade Stone", 0)
        return (
            f"HP: {self.stats.hp}/{self.stats.max_hp} | Uses left: {self._uses_left()}"
            f" | Upgrade Stones: {stones}"
        )

    def _uses_left(self) -> int:
        used = RestRoom.uses_per_floor.get(self.floor, 0)
        return RestRoom.max_uses_per_floor - used

    def _record_use(self) -> None:
        RestRoom.uses_per_floor[self.floor] = RestRoom.uses_per_floor.get(self.floor, 0) + 1
        self._update()

    @staticmethod
    def should_spawn(rests_seen: int) -> bool:
        """Return True if another rest room should spawn on this floor."""

        return rests_seen < RestRoom.min_rests_per_floor

    def _animate(self, message: str) -> None:
        assert self.info_label is not None
        seq = Sequence(
            Func(self.info_label.setText, message),
            Wait(1.0),
            Func(self._update),
        )
        seq.start()

    def exit(self) -> None:
        self.app.scene_manager.switch_to(self.return_scene_factory())
