# Duplicate Handling

## Summary
Handle duplicate character pulls and apply Vitality and stat bonuses.

## Tasks
- [x] Detect duplicates and stack them per character.
- [x] Grant Vitality bonuses with each duplicate according to rules.
- [x] Apply duplicate stacks to relevant stats (e.g., increasing increments by 5% per stack) and enforce stacking behaviour.
- [x] Update save data and roster displays after stacking.
- [x] Document this feature in `.codex/implementation`.
- [x] Add unit tests covering success and failure cases.

## Context
Duplicate logic ensures gacha pulls remain valuable after collecting the roster.

## Testing
- [x] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.
status: ready for review
