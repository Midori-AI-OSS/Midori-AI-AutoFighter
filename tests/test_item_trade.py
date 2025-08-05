from autofighter.gacha.crafting import FOUR_STAR_ITEM
from autofighter.gacha.crafting import TICKET_ITEM
from autofighter.gacha.crafting import trade_items_for_ticket


def test_trade_deducts_items_and_grants_ticket() -> None:
    inventory = {FOUR_STAR_ITEM: 12}
    result = trade_items_for_ticket(inventory)
    assert result is True
    assert inventory[FOUR_STAR_ITEM] == 2
    assert inventory[TICKET_ITEM] == 1


def test_trade_fails_with_insufficient_items() -> None:
    inventory = {FOUR_STAR_ITEM: 9}
    result = trade_items_for_ticket(inventory)
    assert result is False
    assert inventory[FOUR_STAR_ITEM] == 9
    assert TICKET_ITEM not in inventory
