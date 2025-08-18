# Revamp combat UI layout (`91dd0d57`)

## Summary
Battle UI uses a placeholder layout. The interface should place party and foe columns on opposite sides and poll the backend at a frame-rate-controlled interval to avoid unnecessary CPU usage.

## Tasks
- Place party members in a column on the left side of the screen that resizes to show up to five characters.
- Show each party member's stats to the right of their portrait and render HoT/DoT icons beneath.
- Display foes in a column on the right side of the screen that resizes for any enemy count, with stats to the left of portraits and HoT/DoT icons below.
- Use shared fallback art for any party member or foe missing a portrait.
- Poll the backend at a frequency determined by the frame-rate setting, requesting a full party and foe snapshot each tick.
- Parse the snapshot to update the UI while minimizing re-renders.
- Update battle room frontend docs in `.codex/instructions/battle-room.md` with the new layout and polling strategy.

## Context
Feedback item 2 calls for replacing the placeholder combat UI and fetching full party/foe snapshots while being mindful of CPU usage.

Status: Need Review
