# Provide player stat screen endpoint
Expose grouped stats, passives, DoTs, HoTs, and damage types for frontend display. Parent: [Player Stat Screen Plan](../planning/a28124e9-player-stat-screen-plan.md).

## Requirements
- Add a Quart endpoint that returns the player's current stats and status lists.
- Include hooks for passives and effects to append custom lines.
- Respect refresh-rate settings from the options data.

## Acceptance Criteria
- Endpoint responds with structured stat data matching plan categories.
- Tests validate field coverage and refresh-rate clamping.
