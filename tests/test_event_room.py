import importlib
import sys

from pathlib import Path

try:
    importlib.import_module("direct.showbase.MessengerGlobal")
except ModuleNotFoundError:
    import pytest

    pytest.skip("Panda3D not available", allow_module_level=True)

sys.path.append(str(Path(__file__).resolve().parents[1]))

from autofighter.event_room import SAMPLE_EVENTS
from autofighter.stats import Stats


def test_event_deterministic() -> None:
    stats = Stats(hp=5, max_hp=10)
    items: dict[str, int] = {}
    event = SAMPLE_EVENTS[0]
    msg1 = event.resolve(0, stats, items)
    stats2 = Stats(hp=5, max_hp=10)
    items2: dict[str, int] = {}
    msg2 = event.resolve(0, stats2, items2)
    assert msg1 == msg2
    assert stats.hp == stats2.hp
