from __future__ import annotations

from autofighter.gacha.trade_menu import TradeMenu


def test_trade_converts_items_to_tickets() -> None:
    menu = TradeMenu({4: 20})
    gained = menu.trade()
    assert gained == 2
    assert menu.tickets == 2
    assert menu.items[4] == 0


def test_trade_insufficient_items_no_op() -> None:
    menu = TradeMenu({4: 9})
    gained = menu.trade()
    assert gained == 0
    assert menu.tickets == 0
    assert menu.items[4] == 9
