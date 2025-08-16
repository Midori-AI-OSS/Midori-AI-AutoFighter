# Enforce gacha ticket requirements (`a5860221`)

## Summary
The Pulls UI allows draws even when ticket count is 0, enabling free pulls.

## Tasks
- [ ] Add server-side checks that reject pulls without tickets or currency.
- [ ] Update the UI to disable pull buttons and display current ticket counts.
- [ ] Add tests for server validation and UI behavior.

## Context
Feedback highlights a potential exploit where pulls succeed with no tickets.
