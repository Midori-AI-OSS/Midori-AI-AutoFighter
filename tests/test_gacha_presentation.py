from autofighter.gacha.presentation import GachaPresentation
from autofighter.gacha.presentation import GachaResult


def test_single_pull_animation_and_fast_forward() -> None:
    presentation = GachaPresentation(object())
    results = [GachaResult("Ally", 3)]
    shown = presentation.present(results)
    assert shown == results
    assert presentation.animation_played == 3
    assert presentation.display_mode == "single"
    assert presentation.result_labels == []
    presentation.fast_forward_animation()
    texts = [label["text"] for label in presentation.result_labels]
    assert texts == ["Ally (3★)"]
    assert presentation.animation_played == 3


def test_multi_pull_uses_highest_rarity() -> None:
    presentation = GachaPresentation(object())
    results = [
        GachaResult("Ally", 2),
        GachaResult("Becca", 5),
        GachaResult("Carly", 3),
        GachaResult("Daisy", 2),
        GachaResult("Echo", 4),
    ]
    presentation.present(results)
    presentation.fast_forward_animation()
    assert presentation.animation_played == 5
    assert presentation.display_mode == "multi"
    texts = [label["text"] for label in presentation.result_labels]
    assert texts == [
        "1. Ally (2★)",
        "2. Becca (5★)",
        "3. Carly (3★)",
        "4. Daisy (2★)",
        "5. Echo (4★)",
    ]


def test_present_skip_bypasses_animation() -> None:
    presentation = GachaPresentation(object())
    results = [GachaResult("Ally", 6)]
    presentation.present(results, skip=True)
    assert presentation.animation_played is None
    assert presentation.active_interval is None
    texts = [label["text"] for label in presentation.result_labels]
    assert texts == ["Ally (6★)"]


def test_skip_animation_shows_results() -> None:
    presentation = GachaPresentation(object())
    results = [GachaResult("Ally", 4)]
    presentation.present(results)
    assert presentation.active_interval is not None
    presentation.skip_animation()
    assert presentation.active_interval is None
    assert presentation.animation_played is None
    texts = [label["text"] for label in presentation.result_labels]
    assert texts == ["Ally (4★)"]
    assert presentation.last_results == results


def test_fast_forward_preserves_last_results() -> None:
    presentation = GachaPresentation(object())
    results = [GachaResult("Ally", 5)]
    presentation.present(results)
    presentation.fast_forward_animation()
    assert presentation.last_results == results
    assert presentation.animation_played == 5
