# Add player character editor endpoint

## Summary
Quart endpoints now expose player customization. `GET /player/editor` returns
saved pronouns, element, and stat allocations, while `PUT /player/editor`
validates and persists updates. Stats apply to the player roster entry and stat
screen on load.

## Acceptance Criteria
- Pronouns over 15 characters or damage types outside Light, Dark, Wind,
  Lightning, Fire, or Ice are rejected.
- Allocating more than the available stat points returns an error.
- Edits are blocked while a run entry exists in the database.
