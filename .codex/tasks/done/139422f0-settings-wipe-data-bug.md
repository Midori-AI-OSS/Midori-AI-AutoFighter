# Fix settings wipe data button (`139422f0`)

## Summary
The Settings screen's "wipe data" button is unclickable or provides no feedback, leaving saves and roster intact.

## Tasks
- [x] Ensure the wipe-data button triggers the backend wipe endpoint.
- [x] Show confirmation or error messaging after the wipe action.
- [x] Verify the backend removes saves, options, and roster entries.
- [x] Retest UI flows (party picker, inventory) to confirm data is cleared.
- [x] Add tests covering the wipe-data flow and visible feedback.

## Context
Feedback indicates users cannot reliably reset progress or confirm that data was erased.
