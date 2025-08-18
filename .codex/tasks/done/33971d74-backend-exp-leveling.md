# Backend EXP and leveling (`33971d74`)

## Summary
Backend battles do not award experience or handle level progression. Implement formula-based EXP rewards and level requirements, and ensure characters start fresh each run.

## Tasks
- [ ] Award EXP after each battle using `foe_level * 12 + 5 * room_number`.
- [ ] Track room number in battle results so EXP calculation is accurate.
- [ ] Require `(2 ** current_level) * 50` EXP to reach the next level.
- [ ] Reset all characters to level 1 at the start of a new run.
- [ ] On level up, increase stats by `0.3% * new_level` to `0.8% * new_level`, and boost HP by `10 * new_level`, ATK by `5 * new_level`, and DEF by `3 * new_level`.
- [ ] Expose current EXP and level in run and battle responses for frontend display.
- [ ] Add backend tests covering EXP calculation and level-up logic.

## Context
Battle feedback indicates EXP is not awarded, preventing leveling tests and hiding inventory progression.

Status: Need Review
