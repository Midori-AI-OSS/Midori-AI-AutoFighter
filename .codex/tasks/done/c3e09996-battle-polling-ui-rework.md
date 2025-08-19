# Fix Battle Polling and UI Layout

## Summary
The `/rooms/<run_id>/battle` endpoint waits for `BattleRoom.resolve` to finish before replying, so `roomAction(runId, 'battle', 'snapshot')` calls never return during combat. Fighters are misaligned, stats are missing, and navigation lacks a clear handoff after battles. Use Rich to print every action—including HoT/DoT ticks—so testers can spot where async flow stalls.

## Tasks
- [ ] Audit `backend/app.py`'s `battle_room`: it sets `state['battle']=True` and awaits `BattleRoom.resolve`, blocking other requests. Refactor so the battle runs in a background `asyncio` task and the endpoint returns immediately.
- [ ] Implement a `snapshot` action that returns the latest party and foe state while the battle task runs; ensure polling remains responsive throughout combat.
- [ ] Confirm all battle and effect routines (`BattleRoom.resolve`, damage, heals, status ticks) are fully async and avoid blocking calls.
- [ ] Instrument the battle loop with Rich console output for every action—damage, healing, status ticks, and enrage stacks—so halted logs reveal where execution stops.
- [ ] Rework `BattleView` layout so party members appear on the left and foes on the right with visible HP bars and combat stats as described in `.codex/instructions/battle-room.md`.
- [ ] Replace the top-left home icon with a "Next Room" button once battle rewards are resolved; keep the battle view visible until the player chooses to advance.
- [ ] Add a planned "battle review" screen that summarizes damage and healing done by each combatant, and document the feature in `.codex/instructions/battle-room.md`.
- [ ] Update `README.md` and relevant `.codex/implementation` docs if new dependencies or behavior changes are introduced.

## References
- `.codex/instructions/battle-room.md`


Status: Need Review
