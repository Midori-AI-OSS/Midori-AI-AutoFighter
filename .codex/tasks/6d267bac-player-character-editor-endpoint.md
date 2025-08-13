# Add player character editor endpoint
Provide backend APIs for setting the player's pronouns, base damage type, and allocating starting stats. Parent: [UI Foundation](../planning/e26e5ed7-ui-foundation-plan.md).

## Requirements
- Create Quart endpoints to fetch and update player pronouns, damage type, and stat points.
- Validate allocations against available points and required 4★ upgrade items for bonus points.
- Reject edits if a run is active so stats remain fixed mid-run.
- Persist changes in the encrypted save database.
- Accept free-form pronoun strings up to 15 characters from the frontend.
- Allow choosing a damage type from Light, Dark, Wind, Lightning, Fire, or Ice; changes are free but blocked during runs. Luna's Generic type cannot be selected.

## Acceptance Criteria
- Endpoints return updated player data and reject invalid allocations or mid-run edits.
- Pronouns over 15 characters or attempts to select Generic, Luna's damage type, are rejected.
- Tests cover success, over-allocation, missing upgrade items, blocked edits during runs, and invalid pronouns or damage types.
