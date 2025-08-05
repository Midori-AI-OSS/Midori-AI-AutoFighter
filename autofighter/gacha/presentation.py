from __future__ import annotations

from dataclasses import dataclass

try:
    from direct.gui.DirectGui import DirectFrame
    from direct.gui.DirectGui import DirectLabel
    from direct.interval.IntervalGlobal import Func
    from direct.interval.IntervalGlobal import Sequence
    from direct.interval.IntervalGlobal import Wait
except Exception:  # pragma: no cover - allow headless tests
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

    class DirectFrame(_Widget):  # type: ignore[dead-code]
        pass

    class DirectLabel(_Widget):  # type: ignore[dead-code]
        pass

    class Sequence:  # type: ignore[dead-code]
        def __init__(self, *_: object) -> None:
            pass

        def start(self) -> None:
            pass

        def finish(self) -> None:
            pass

    class Wait:  # type: ignore[dead-code]
        def __init__(self, *_: object) -> None:
            pass

    class Func:  # type: ignore[dead-code]
        def __init__(self, func, *args: object, **kwargs: object) -> None:
            self.func = func
            self.args = args
            self.kwargs = kwargs

        def __call__(self) -> None:
            self.func(*self.args, **self.kwargs)

from autofighter.gui import TEXT_COLOR
from autofighter.gui import FRAME_COLOR
from autofighter.gui import WIDGET_SCALE
from autofighter.gui import set_widget_pos


@dataclass
class GachaResult:
    """Simple container for a gacha pull result."""

    name: str
    rarity: int


class GachaPresentation:
    """Display gacha results with rarity-based animations."""

    _ANIMATION_TIME = {
        1: 0.5,
        2: 0.5,
        3: 0.5,
        4: 1.0,
        5: 1.5,
        6: 2.0,
    }

    def __init__(self, app) -> None:
        self.app = app
        self.animation_played: int | None = None
        self.display_mode: str = "single"
        self.last_results: list[GachaResult] = []
        self._interval: Sequence | None = None
        self._frame: DirectFrame | None = None
        self.result_labels: list[DirectLabel] = []

    def play_animation(self, rarity: int) -> None:
        if self._interval:
            self._interval.finish()
        duration = self._ANIMATION_TIME.get(rarity, 0.5)
        self.animation_played = rarity
        self._interval = Sequence(Wait(duration))
        try:  # pragma: no cover - Panda3D only
            self._interval.start()
        except Exception:
            pass

    def skip_animation(self) -> None:
        if self._interval:
            try:  # pragma: no cover - Panda3D only
                self._interval.finish()
            except Exception:
                pass
            self._interval = None
        self.animation_played = None

    def clear_results(self) -> None:
        if self._frame:
            self._frame.destroy()
        self._frame = None
        self.result_labels.clear()

    def show_results(self, results: list[GachaResult]) -> list[GachaResult]:
        self.clear_results()
        self.last_results = results
        self.display_mode = "multi" if len(results) > 1 else "single"
        self._frame = DirectFrame(frameColor=FRAME_COLOR)
        for i, result in enumerate(results):
            label = DirectLabel(
                text=f"{result.name} ({result.rarity}\u2605)",
                text_fg=TEXT_COLOR,
                parent=self._frame,
                scale=WIDGET_SCALE,
            )
            set_widget_pos(label, (0, 0, 0.15 * (len(results) - 1 - i)))
            self.result_labels.append(label)
        return results

    def present(self, results: list[GachaResult], skip: bool = False) -> list[GachaResult]:
        if not results:
            self.skip_animation()
            self.clear_results()
            return []

        if skip:
            self.skip_animation()
        else:
            highest = max(r.rarity for r in results)
            self.play_animation(highest)

        return self.show_results(results)

    @property
    def active_interval(self) -> Sequence | None:
        return self._interval
