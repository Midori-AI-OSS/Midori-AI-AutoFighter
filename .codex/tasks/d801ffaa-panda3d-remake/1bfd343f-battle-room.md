# Battle Room Implementation

## Summary
Create the combat room with turn-based foe interactions.

## Tasks
- [x] Render player and foe models or placeholders using Panda3D node graphs.
- [x] Implement turn-based logic using messenger events and the shared `Stats` dataclass for accuracy and damage.
- [x] Scale foes according to floor, room, Pressure level, and loop count.
- [x] Display damage numbers, status effect icons, and reusable attack effects.
- [x] Trigger overtime warnings after 100 turns (500 for floor bosses) with red/blue flashes and an `Enraged` buff.
- [ ] Document this feature in `.codex/implementation`.
- [ ] Add unit tests covering success and failure cases.

## Context
Battle rooms are the core gameplay loop and must mirror current mechanics.

## Testing
- [x] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.

status: failed - turn counter advances only on player actions and overtime buffs never trigger correctly
