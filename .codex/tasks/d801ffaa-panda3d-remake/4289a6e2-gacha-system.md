# Gacha System

## Summary
Implement the character gacha with escalating odds and upgrade-item rewards.

## Tasks
- [ ] Seed the pull pool with existing player plugins and allow 1, 5, or 10 pulls.
- [ ] Play a skippable video keyed to the highest rarity obtained and show a results menu afterward.
- [ ] Apply pity logic starting at 0.001%, rising to ~5% at pull 159, and guaranteeing the featured character at 180 pulls.
- [ ] Handle duplicate logic: 25% chance before completing the 5★ roster, weighted duplicates after the roster is full.
- [ ] Grant upgrade items on failed pulls based on damage types, with item costs for upgrading and trading 10×4★ items for an extra pull.
- [ ] Implement Vitality bonus stacking for duplicates (0.01% first, each increment +5% more than the last).
- [ ] Serialize rewards, pity counts, and character stacks for persistence.

## Context
The gacha provides new characters and progression outside runs.

## Testing
- [ ] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.
