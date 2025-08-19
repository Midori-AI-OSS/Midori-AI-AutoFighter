# Ensure combat UI shows complete stats (`196c35d9`)

## Summary
The combat interface does not reliably display all expected stats, and related documentation no longer reflects the intended layout. Revise the battle view so both party members and foes render identical stat blocks, and update docs to match.

## Tasks
- Audit `BattleView.svelte` to verify party and foe columns list HP, Attack, Defense, Mitigation, and Crit rate next to each portrait.
- Add missing stats or adjust ordering so party and foe layouts mirror each other.
- Keep HoT/DoT markers beneath portraits and ensure fallback art appears when images are absent.
- Poll the backend each frame-rate tick for full snapshot data and minimize unnecessary re-renders.
- Update `.codex/implementation/battle-view.md` and `frontend/README.md` with the corrected stat list and layout details.
- Revise `.codex/instructions/battle-room.md` so combat UI guidance matches the updated implementation.

## Context
Work from `91dd0d57-combat-ui-layout` was not fully applied; this follow-up restores the intended layout and keeps documentation in sync.

Status: Need Review
