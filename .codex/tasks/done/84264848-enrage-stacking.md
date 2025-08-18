# Implement stacking enrage buff (`84264848`)

## Summary
Foes only receive a one-time 40% attack increase when overtime triggers. They should gain an additional 40% `Enraged` attack buff each turn after enrage begins.

## Tasks
- Detect enrage start (100 turns for normal foes, 500 for floor bosses) in the backend battle loop.
- After enrage starts, add a 40% attack multiplier to all foes each turn and mark the effect as an `Enraged` status.
- Expose the current enrage stack count and status in the battle payload for the frontend.
- Notify the frontend when enrage is active so it can react visually.
- In the battle UI, gradually cycle the background between blue and red while enrage is active and reset once combat ends.
- Add backend tests verifying attack increases stack every turn post-enrage.
- Add frontend tests confirming the background color transition when enrage triggers.
- Update `.codex/instructions/battle-room.md` to document stacking enrage behavior and the new UI effect.

## Context
Feedback item 1 questions whether enrage stacking exists. Battle docs only mention a single 40% buff.

Status: Need Review
