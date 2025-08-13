# Persist random damage types
Ensure characters with random damage types keep the same type across loads. Parent: [Web GUI and Quart Game Plan](../planning/8a7d9c1e-web-game-plan.md).

## Requirements
- Randomly assign a damage type the first time a character with a random type is created or loaded.
- Save the assigned type in the encrypted database so future loads reuse it.
- Apply to the player character and any plugins flagged for random damage types.

## Acceptance Criteria
- Reloading a character does not change its damage type.
- Tests verify that a random type is chosen only once and persists across sessions.
