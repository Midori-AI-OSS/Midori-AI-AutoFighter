# Track shop purchases for the whole party
Fix room logic so bought items apply to the entire party rather than only the first member. Parent: [Web Game Plan](../planning/8a7d9c1e-web-game-plan.md).

## Requirements
- Record purchased items in a shared inventory accessible by every party member.
- Deduct gold from the single party-wide gold pool and persist inventory in saves.
- Update room endpoint documentation to reflect shared inventory behavior.

## Acceptance Criteria
- Buying an item adds it once to party inventory and appears for all members.
- Tests cover purchasing and inventory persistence across rooms.
