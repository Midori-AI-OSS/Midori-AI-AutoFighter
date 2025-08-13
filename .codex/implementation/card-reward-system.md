# Card Reward System

Battles grant unique cards that permanently boost party stats. Cards come in star
ranks and only one copy of each can be owned. Victories present three unused
cards of the appropriate star rank; choosing one adds it to the party's inventory.
Card and relic bonuses now apply at the start of each combat rather than on
acquisition so higher-star effects trigger correctly. Subsequent battles skip
duplicates by rolling only from cards not yet collected.

## Testing
- `uv run pytest backend/tests/test_card_rewards.py`
