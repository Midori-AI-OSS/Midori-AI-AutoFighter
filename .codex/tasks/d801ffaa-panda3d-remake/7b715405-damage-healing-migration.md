# Damage and Healing Migration

## Summary
Port existing damage-over-time and healing-over-time systems to the new architecture.

## Tasks
- [x] Define a shared `Stats` dataclass for players and foes.
- [x] Reimplement DoT and HoT handling using Panda3D-friendly data structures.
- [x] Support the following DoTs with their effects: Bleed, Celestial Atrophy, Abyssal Corruption, Abyssal Weakness, Gale Erosion, Charged Decay, Frozen Wound, Blazing Torment, Cold Wound (5-stack cap), Twilight Decay, Impact Echo.
- [x] Support HoTs: Regeneration, PlayerName's Echo, PlayerName's Heal.
- [x] Ensure stacking and reset rules match the current game's mechanics and clear after battles unless made permanent.
- [x] Add unit tests for each damage and healing type.
- [ ] Document this feature in `.codex/implementation`.
- [ ] Add unit tests covering success and failure cases.

## Context
Consistent damage and healing logic keeps combat behavior aligned with the original game.

## Testing
- [x] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.

status: in progress
