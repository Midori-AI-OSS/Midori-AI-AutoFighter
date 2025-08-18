# Make battle loop fully async with 0.5s turns (`90f1f578`)

## Summary
Current combat loop uses blocking logic and inconsistent sleep times. Refactor to ensure HoTs, DoTs, damage, healing, and regens are awaitable and enforce a 0.5s turn cadence.

## Tasks
- [x] Convert `Stats.apply_damage`, `Stats.apply_healing`, `Stats.maybe_regain`, and `EffectManager.tick/on_action` to async functions.
- [x] Replace blocking operations with `await` calls or background tasks.
- [x] Adjust `rooms.BattleRoom.resolve` to await these operations and ensure each turn lasts at least 0.5 s, sleeping only if the turn finishes early.
- [x] Add tests covering async flow and timing.
- [x] Update docs describing async battle processing.

## Context
Players experience delays and blocking during combat; making the loop async with fixed pacing should smooth gameplay.

Status: Need Review
