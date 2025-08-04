# Damage and Healing Migration

## Summary
Port existing damage-over-time and healing-over-time systems to the new architecture.

## Tasks
- [ ] Reimplement DoT and HoT handling using Panda3D-friendly data structures.
- [ ] Ensure stacking and reset rules match the current game's mechanics.
- [ ] Add unit tests for each damage and healing type.

## Context
Consistent damage and healing logic keeps combat behavior aligned with the original game.

## Testing
- [ ] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.
