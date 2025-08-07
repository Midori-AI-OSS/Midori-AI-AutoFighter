from __future__ import annotations

from autofighter.stat_screen import StatScreen
from autofighter.stats import Stats


class DummyApp:
    def __init__(self) -> None:
        self.scene_manager = object()
        self.stat_refresh_rate = 5


def test_stat_screen_renders_groups(monkeypatch) -> None:
    texts: list[str] = []

    class DummyText:
        def __init__(self, text: str, **_kwargs) -> None:
            self.text = text
            texts.append(text)

        def destroy(self) -> None:  # pragma: no cover - cleanup placeholder
            pass

    monkeypatch.setattr("autofighter.stat_screen.OnscreenText", DummyText)
    screen = StatScreen(DummyApp(), Stats(hp=5, max_hp=10))
    screen._render()
    expected = {
        "Core:",
        "Offense:",
        "Defense:",
        "Vitality & Advanced:",
        "Status:",
    }
    lines = set(texts)
    assert expected.issubset(lines)


def test_stat_screen_uses_app_refresh_rate() -> None:
    app = DummyApp()
    app.stat_refresh_rate = 7
    screen = StatScreen(app, Stats(hp=1, max_hp=1))
    assert screen.refresh_rate == 7


def test_stat_screen_clamps_refresh_rate() -> None:
    app = DummyApp()
    app.stat_refresh_rate = 20
    screen = StatScreen(app, Stats(hp=1, max_hp=1))
    assert screen.refresh_rate == 10

def test_stat_screen_clamps_low_refresh_rate() -> None:
    app = DummyApp()
    app.stat_refresh_rate = 0
    screen = StatScreen(app, Stats(hp=1, max_hp=1))
    assert screen.refresh_rate == 1
