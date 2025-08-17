# Enforce gacha ticket requirements (`a5860221`)

## Summary
The Pulls UI allows draws even when ticket count is 0, enabling free pulls.

## Tasks
- [x] Add server-side checks that reject pulls without tickets or currency.
- [x] Update the UI to disable pull buttons and display current ticket counts.
- [x] Capture and document network requests and responses when pulls are attempted with insufficient tickets to verify server handling.
- [x] Add tests for server validation and UI behavior.

## Context
Feedback highlights a potential exploit where pulls succeed with no tickets.
