# Duplicate Handling

## Summary
Handle duplicate character pulls and apply Vitality and stat bonuses.

## Tasks
- [ ] Detect duplicates and stack them per character.
- [ ] Grant Vitality bonuses with each duplicate according to rules.
- [ ] Apply duplicate stacks to relevant stats (e.g., increasing increments by 5% per stack) and enforce stacking behaviour.
- [ ] Update save data and roster displays after stacking.
- [ ] Document this feature in `.codex/implementation`.
- [ ] Add unit tests covering success and failure cases.

## Context
Duplicate logic ensures gacha pulls remain valuable after collecting the roster.

## Testing
- [ ] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.
status: in progress
