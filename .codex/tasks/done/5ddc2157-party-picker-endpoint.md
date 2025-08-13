# Add party picker endpoint for run setup

## Summary
Quart endpoint now accepts a roster of 1–5 owned character IDs and optional player damage type to begin a run. The response returns the run ID, map data, and passive names for each party member.

## Acceptance Criteria
- Endpoint rejects invalid rosters and damage types.
- Starting a run with a valid party persists the player's element and returns party data.
- Tests verify roster validation, damage type persistence, and size limits.
