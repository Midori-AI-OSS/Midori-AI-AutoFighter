# Implement relic drop picker and spawn rates (`d1205a6e`)

## Summary
Backend should roll for relic drops after battles and, when a relic is awarded, send three random relic options to the frontend. The frontend must display a relic picker using images from the relic folder with star-rank tinting like cards.

## Tasks
- [x] Define relic drop rate table and hook it into battle rewards.
- [x] Return three relic choices with image paths and star ranks when a relic drops.
- [x] Display a relic picker on the frontend mirroring card tint styles and allow selection.
- [x] Persist chosen relic to the run state and inventory.
- [x] Document relic picker flow.

## Context
Players currently receive relics silently with no choice or visuals; a picker enhances engagement and mirrors card rewards.

Status: Need Review
