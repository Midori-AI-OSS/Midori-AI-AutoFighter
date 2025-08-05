from __future__ import annotations

from autofighter.gacha.presentation import GachaResult
from autofighter.gacha.presentation import GachaPresentation


def test_single_pull_triggers_correct_animation() -> None:
    presentation = GachaPresentation(object())
    results = [GachaResult("Ally", 3)]
    shown = presentation.present(results)
    assert presentation.animation_played == 3
    assert presentation.display_mode == "single"
    assert shown == results


def test_multi_pull_uses_highest_rarity() -> None:
    presentation = GachaPresentation(object())
    results = [GachaResult("Ally", 2), GachaResult("Becca", 5)]
    shown = presentation.present(results)
    assert presentation.animation_played == 5
    assert presentation.display_mode == "multi"
    assert shown == results


def test_skip_skips_animation() -> None:
    presentation = GachaPresentation(object())
    results = [GachaResult("Ally", 6)]
    presentation.present(results, skip=True)
    assert presentation.animation_played is None
    assert presentation.display_mode == "single"
