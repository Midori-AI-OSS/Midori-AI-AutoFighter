from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GachaResult:
    """Simple container for a gacha pull result."""

    name: str
    rarity: int


class GachaPresentation:
    """Display gacha results with rarity-based animations."""

    def __init__(self, app) -> None:
        self.app = app
        self.animation_played: int | None = None
        self.display_mode: str = "single"
        self.last_results: list[GachaResult] = []

    def play_animation(self, rarity: int) -> None:
        self.animation_played = rarity

    def show_results(self, results: list[GachaResult]) -> list[GachaResult]:
        self.last_results = results
        self.display_mode = "multi" if len(results) > 1 else "single"
        return results

    def present(self, results: list[GachaResult], skip: bool = False) -> list[GachaResult]:
        if not results:
            self.animation_played = None
            return []

        if not skip:
            highest = max(r.rarity for r in results)
            self.play_animation(highest)
        else:
            self.animation_played = None

        return self.show_results(results)
