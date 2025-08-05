from autofighter.gacha.crafting import trade_for_ticket
from autofighter.gacha.crafting import upgrade


def test_upgrade_success() -> None:
    inventory = {1: 125}
    assert upgrade(inventory, 1)
    assert inventory[1] == 0
    assert inventory[2] == 1


def test_upgrade_failure() -> None:
    inventory = {1: 124}
    assert not upgrade(inventory, 1)
    assert inventory[1] == 124
    assert 2 not in inventory


def test_trade_for_ticket_success() -> None:
    inventory = {4: 10}
    assert trade_for_ticket(inventory)
    assert inventory[4] == 0
    assert inventory["tickets"] == 1


def test_trade_for_ticket_failure() -> None:
    inventory = {4: 9}
    assert not trade_for_ticket(inventory)
    assert inventory[4] == 9
    assert "tickets" not in inventory

