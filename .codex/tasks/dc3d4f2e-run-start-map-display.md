# Run start and map display (`dc3d4f2e`)

## Summary
Trigger a run from Start/Load Run and show a basic floor map.

## Tasks
- Start the gameplay loop when Start/Load Run is selected.
- Open the party picker before showing the floor map.
- [x] Present a simple floor map to choose rooms.

## Context
Builds on the main menu to enable initial exploration.

## Notes
Map view now uses `MapDisplay.svelte` with `lucide-svelte` icons inside
`MenuPanel`. Party picker will be added separately.
