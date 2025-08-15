# Send Room Selection to Backend Battle Endpoint

## Summary
Clicking a room on the map currently does nothing. Selecting a room should trigger the component responsible for backend communication and send the expected JSON payload to the correct room endpoint.

## Instructions
- Identify the frontend component that handles room selection.
- Call the matching endpoint for the room's `room_type` (`/rooms/{run_id}/battle`, `/shop`, `/rest`, or `/boss`) with `{ "action": "" }` or any required fields.
- Document the expected JSON format in implementation notes.

## Context
Enables battles to start when a player chooses a room, completing the basic run loop.
