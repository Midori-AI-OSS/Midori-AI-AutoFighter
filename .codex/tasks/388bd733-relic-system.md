# Implement relic system
Add permanent passive relics that stack without cap. Parent: [Relic Plan](../planning/bd48a561-relic-plan.md).

## Requirements
- Represent relic stacks and star ranks in saves.
- Apply relic effects automatically on run start and during battles.
- Drop relics from room rewards with star-based odds.

## Acceptance Criteria
- Collected relics persist across rooms and modify combat stats.
- Tests cover stacking behavior and reward serialization.
