# Item Bonus Confirmation

## Summary
Ensure upgrade-item stat bonuses persist after player creation and properly consume items.

## Tasks
- [ ] Track 4★ upgrade item spending and apply bonus stat points.
- [ ] Warn when items are insufficient or bonuses exceed limits.
- [ ] Persist purchased bonuses to saves and the stat screen.
- [ ] Document this feature in `.codex/implementation`.
- [ ] Add unit tests covering success and failure cases.

## Context
Players should not lose items or bonuses during character creation.

## Testing
- [ ] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.
status: in progress
