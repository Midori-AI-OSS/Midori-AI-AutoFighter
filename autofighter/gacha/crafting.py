from __future__ import annotations

from typing import Dict


def craft_upgrades(items: Dict[int, int]) -> None:
    """Convert 125 lower-star items into one higher star in-place."""
    for star in (1, 2, 3):
        while items.get(star, 0) >= 125:
            items[star] -= 125
            items[star + 1] = items.get(star + 1, 0) + 1


def trade_for_tickets(items: Dict[int, int]) -> int:
    """Trade groups of ten 4★ items for gacha tickets.

    Returns the number of tickets granted and mutates ``items``.
    """
    tickets = 0
    while items.get(4, 0) >= 10:
        items[4] -= 10
        tickets += 1
    return tickets
