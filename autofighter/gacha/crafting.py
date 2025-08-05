from __future__ import annotations

from typing import MutableMapping


Inventory = MutableMapping[int | str, int]

COST_PER_UPGRADE = 125
COST_PER_TICKET = 10


def upgrade(inventory: Inventory, star: int) -> bool:
    """Convert ``125`` items of ``star`` into one ``star + 1`` item."""

    if inventory.get(star, 0) < COST_PER_UPGRADE:
        return False
    inventory[star] -= COST_PER_UPGRADE
    inventory[star + 1] = inventory.get(star + 1, 0) + 1
    return True


def trade_for_ticket(inventory: Inventory) -> bool:
    """Trade ``10`` 4★ items for one gacha ticket."""

    if inventory.get(4, 0) < COST_PER_TICKET:
        return False
    inventory[4] -= COST_PER_TICKET
    inventory["tickets"] = inventory.get("tickets", 0) + 1
    return True

