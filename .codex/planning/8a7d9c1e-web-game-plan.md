# Web GUI and Quart Game Plan

## Goal
Transition Midori AI AutoFighter to a web-based architecture. The game's logic remains in Python, served through a Quart server, while the user interface runs in a separate Svelte frontend. The project no longer targets 3D rendering.

Status: ready for audit.

## Project Lead Feedback
- Use Svelte for the frontend, keeping the main menu's high-contrast icon grid inspired by Arknights.
- Use Lucide or equivalent icons with clear labels and ensure layouts scale across desktop and mobile resolutions.
- Reuse existing plugin-driven combat, menus, stat screens, and multi-room run map.
- Manage the JS frontend and Quart backend with Docker Compose.
- Keep `myunderstanding.md` current with gameplay flow updates.

## Current Issues
- Passive plugin system, relics, and card rewards are missing.
- Gacha pulls and character recruitment are absent; endpoints must be accessible from the main menu and rest nodes, sharing pity and currency, with recruits usable immediately during that rest.
- Player stat screen endpoint is not exposed.
- Shop endpoint handles purchases but only stores items on the first party member.
- Player character editor and party picker endpoints are not implemented; the editor needs free-text pronouns (≤15 chars) and free damage-type selection among Light, Dark, Wind, Lightning, Fire, or Ice. Luna uses a unique Generic type that players cannot pick, and stats lock during runs. The picker should return passive summaries, accept flexible party sizes, and let the player switch to any of those non-Generic types before starting a run.
- Characters with random damage types change on every load; assigned types must persist.

## Immediate Playable Flow
1. Wire passive, relic, and card systems into combat.
2. Add gacha recruitment (usable from the main menu and rest nodes sharing pity and currency), player stat screen endpoint, and shared party inventory.
3. Persist randomly assigned damage types and allow players to freely choose their own outside runs from Light, Dark, Wind, Lightning, Fire, or Ice.
4. Implement player character editor (free-text pronouns up to 15 characters and damage-type choice excluding Luna's Generic type with pre-run stat allocation) and party picker (passive info, damage-type switching among the six non-Generic types, 1–5 party size) before starting runs.

## Detailed Plans
Detailed planning documents will be written once the playable flow is in place.

## Notes
- Repository intentionally ships without `save.db` and omits a Compose volume.
- Compose profiles intentionally reuse host port `59002`.
- `Dockerfile.python` uses `$(whoami)` and chains `yay` commands with `&&`; both are intentional and require no changes.
