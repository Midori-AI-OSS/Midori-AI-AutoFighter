# Gacha System

Provides recruitment pulls and item conversion utilities.

## Crafting and Trade
- `trade_items_for_ticket(inventory: dict[str, int], *, item_name: str = "4★ Upgrade Item", ticket_name: str = "Gacha Ticket", rate: int = 10)` – converts ``rate`` 4★ upgrade items into one gacha ticket. Returns ``True`` on success.
- UI exposes a **Trade 10x4★ for Ticket** button calling this helper.
