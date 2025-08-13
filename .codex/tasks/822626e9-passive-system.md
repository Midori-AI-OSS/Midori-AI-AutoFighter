# Integrate passive plugin system
Port passive plugins and loader to the new backend. Parent: [Passive System Plan](../planning/a6e7f4bd-passive-system-plan.md).

## Requirements
- Discover `plugins/passives` and register triggers with stack limits.
- Expose hooks in combat and rooms for passives to modify stats or apply effects.
- Surface active passives on the stat screen data.

## Acceptance Criteria
- Sample passive plugins trigger during battles and map events.
- Tests confirm discovery, stacking behavior, and trigger resolution.
