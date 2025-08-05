# Player Stat Screen

## Summary
Develop a detailed stat screen showing core, offensive, defensive, vitality, advanced, and status data.

## Tasks
- [x] Display core stats: HP, Max HP, EXP, Level, EXP buff multiplier, Actions per Turn.
- [x] Show offense stats: Attack, Crit Rate, Crit Damage, Effect Hit Rate, base damage type.
- [x] Show defense stats: Defense, Mitigation, Regain, Dodge Odds, Effect Resistance.
- [x] Show vitality and advanced stats including Action Points, cumulative damage taken/dealt, and kills.
- [x] List active passives, DoTs, HoTs, damage types, and relic stacks, including all effects from the planning document.
- [x] Refresh the screen at a user-defined rate (default every 5 frames, adjustable 1–10).
- [x] Allow ESC or close to return to the previous scene, respecting the Options pause setting.
- [x] Expose hooks for plugins to append custom lines to the Status section.
- [ ] Document this feature in `.codex/implementation`.
- [ ] Add unit tests covering success and failure cases.

## Context
A comprehensive stat screen helps players track progression and effects.

## Testing
- [x] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.

status: in progress
