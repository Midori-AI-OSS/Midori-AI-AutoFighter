from __future__ import annotations


FOUR_STAR_ITEM = "4★ Upgrade Item"
TICKET_ITEM = "Gacha Ticket"
ITEMS_PER_TICKET = 10


def trade_items_for_ticket(
    inventory: dict[str, int],
    *,
    item_name: str = FOUR_STAR_ITEM,
    ticket_name: str = TICKET_ITEM,
    rate: int = ITEMS_PER_TICKET,
) -> bool:
    """Exchange 4★ items for a gacha ticket.

    Deducts ``rate`` of ``item_name`` and increments ``ticket_name``.
    Returns ``True`` if the trade succeeds.
    """
    if inventory.get(item_name, 0) < rate:
        return False
    inventory[item_name] -= rate
    inventory[ticket_name] = inventory.get(ticket_name, 0) + 1
    return True
