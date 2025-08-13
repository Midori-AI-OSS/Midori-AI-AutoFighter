# Add party picker endpoint for run setup
Allow the frontend to submit a roster of one to five characters including the player before starting a run and let the player switch damage type. Parent: [UI Foundation](../planning/e26e5ed7-ui-foundation-plan.md).

## Requirements
- Add a Quart endpoint that accepts selected character IDs and validates ownership and duplicates.
- Include passive descriptions for each selected character in the response.
- Initialize a new run with the chosen party and return run data.
- Allow changing the player's damage type to any of Light, Dark, Wind, Lightning, Fire, or Ice before confirming the party; Luna's Generic type is off-limits.

## Acceptance Criteria
- Endpoint rejects invalid rosters and starts runs with valid parties.
- Response includes passive summaries for each character.
- Tests verify size limits and ownership checks.
- Tests cover damage type changes for the player and reject Generic, Luna's type, as an option.
