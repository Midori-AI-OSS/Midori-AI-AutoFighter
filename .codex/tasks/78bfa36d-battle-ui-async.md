# Fix Battle UI layout, polling, and backend async

## Summary
- Frontend battle scenes still render foes on the left despite prior fixes. Audit markup and styles so `party-column` renders on the left and `foe-column` on the right, matching the reference screenshot and docs.
- Polling for battle snapshots is capped at a 50 ms floor, ignoring framerate settings. Rework the timer so 30/60/120 fps options are honored exactly and adjust tests accordingly.
- The battle endpoint mixes async code with synchronous database calls. Refactor to avoid blocking the event loop and keep frame‑rate polling responsive.

## References
- [frontend/src/lib/BattleView.svelte – polling](../../frontend/src/lib/BattleView.svelte#L13-L41)
- [frontend/src/lib/BattleView.svelte – layout columns](../../frontend/src/lib/BattleView.svelte#L60-L127)
- [frontend/src/lib/BattleView.svelte – foe row-reverse](../../frontend/src/lib/BattleView.svelte#L167-L168)
- [frontend/src/lib/SettingsMenu.svelte – framerate options](../../frontend/src/lib/SettingsMenu.svelte#L102-L109)
- [frontend/src/lib/GameViewport.svelte – framerate persistence](../../frontend/src/lib/GameViewport.svelte#L33-L57)
- [frontend/src/lib/settingsStorage.js – numeric coercion](../../frontend/src/lib/settingsStorage.js#L3-L20)
- [frontend/tests/battleview.test.js – layout & polling tests](../../frontend/tests/battleview.test.js#L1-L38)
- [frontend/tests/frameratePersistence.test.js – saved framerate](../../frontend/tests/frameratePersistence.test.js#L5-L9)
- [backend/app.py – battle endpoint](../../backend/app.py#L653-L778)
- [docs: .codex/implementation/battle-view.md](../implementation/battle-view.md#L3-L16)
- [docs: .codex/instructions/battle-room.md](../instructions/battle-room.md#L11-L18)

## Tasks
1. **Frontend: BattleView layout**
   - Inspect lines 60‑127 where `party-column` and `foe-column` are rendered. The party column must appear first in DOM order and stay on the left while foes occupy the right column.
   - At lines 84‑90 and 97‑102, stats for party and foes are mirrored. Confirm `row-reverse` at lines 167‑168 only flips foe flex order and does not invert columns globally.
   - Compare final render with the reference screenshot. Update markup or CSS if foes still appear on the left.
   - Expand `frontend/tests/battleview.test.js` to assert `.party-column` is the first child and `.foe-column` the second.
2. **Frontend: BattleView polling**
   - Lines 13‑14 compute `pollDelay` from `framerate`; line 41 uses `Math.max(50, pollDelay - duration)` which enforces a 50 ms minimum.
   - Replace the hardcoded floor so polling strictly matches user settings: use `setTimeout(fetchSnapshot, Math.max(0, pollDelay - duration))` or similar.
   - Verify the `framerate` prop is sourced from `GameViewport` (lines 33 & 57) and that SettingsMenu options (lines 102‑109) and `settingsStorage.js` (lines 3‑20) persist numeric values.
   - Expand frontend tests to measure snapshot intervals ~33 ms, 17 ms, and 8 ms (±10%) for 30/60/120 fps settings, and ensure framerate persistence via `frameratePersistence.test.js`.
3. **Backend: battle endpoint async**
   - In `app.py` lines 653‑778, identify blocking operations: `load_party`/`load_map` (702‑703) and `save_map`/`save_party` (679‑680, 750) are synchronous.
   - Move these calls to an executor (`asyncio.to_thread` or `loop.run_in_executor`) or adopt an async database driver (`aiosqlite`) so `_run_battle` can progress without blocking.
   - Ensure turn delays rely on `asyncio.sleep` and scale with client frame rate to keep 30/60/120 fps polling responsive.
4. **Doc sync**
   - After code changes, update `.codex/implementation/battle-view.md` and `.codex/instructions/battle-room.md` to reflect final layout, polling behavior, and async strategy.

## Testing
- `bun test frontend/tests/battleview.test.js`
- `uv run pytest backend/tests/test_battle_timing.py`

