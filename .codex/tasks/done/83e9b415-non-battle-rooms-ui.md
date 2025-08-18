# Implement non-battle room UIs (`83e9b415`)

## Summary
When the backend selects a shop or rest room, the frontend lacks dedicated interfaces. Players need screens for purchasing items and resting without entering battles.

## Tasks
- Use the existing card/relic reward pop-up layout as a template to build a shop room UI showing items, prices, and purchase buttons from backend inventory data.
- Create a rest room UI on the same pop-up foundation that supports gacha pulls and party swapping within documented limits.
- Display the player's current currency or resources inside these interfaces.
- Ensure room selection logic routes to the correct UI when the backend indicates a shop or rest room.
- Add frontend tests that enter each room type and verify purchasing and resting actions.
- Update `.codex/instructions/shop-room.md` and `.codex/instructions/rest-room.md` with notes on the new UIs and their pop-up behavior.

## Context
Feedback item 6 asks how the app handles non-battle rooms and requests UIs for shops and rest rooms.

Status: Need Review
