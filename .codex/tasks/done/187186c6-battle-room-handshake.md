# Backend waits for explicit next room (`187186c6`)

## Summary
Backend auto-advances after battles causing desync with frontend. Implement handshake so server pauses until frontend requests the next room.

## Tasks
- [x] Add state in run data to mark completion and await "next room" trigger.
- [x] Expose endpoint for frontend to signal readiness to proceed.
- [x] Update frontend `+page.svelte` to send explicit "next" when battle results processed.
- [x] Document new flow in `.codex/implementation` and README.

## Context
User reports backend proceeding before frontend is ready, leading to mismatched room states between fights.

Status: Need Review
