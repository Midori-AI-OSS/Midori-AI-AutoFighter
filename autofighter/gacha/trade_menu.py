from __future__ import annotations

from typing import Dict

from .crafting import trade_for_tickets


class TradeMenu:
    """Menu for trading 4★ upgrade items for gacha tickets."""

    def __init__(self, items: Dict[int, int] | None = None, tickets: int = 0) -> None:
        self.items = items or {4: 0}
        self.tickets = tickets

    def trade(self) -> int:
        """Exchange groups of ten 4★ items for tickets.

        Returns the number of tickets gained."""

        gained = trade_for_tickets(self.items)
        self.tickets += gained
        return gained
