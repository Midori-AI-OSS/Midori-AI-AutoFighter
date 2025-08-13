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
- No encrypted save database for persisting runs and inventory.
- Map generator and room types are unimplemented.
- Passive plugin system, relics, and card rewards are missing.
- Gacha pulls and character recruitment are absent.
- Player stat screen endpoint is not exposed.
- Shop endpoint handles purchases but only stores items on the first party member.

## Immediate Playable Flow
1. Implement encrypted saves and shared party inventory.
2. Generate maps with battle, shop, rest, chat, and boss rooms.
3. Wire passive, relic, and card systems into combat.
4. Add gacha recruitment and a stat screen endpoint.

## Detailed Plans
Detailed planning documents will be written once the playable flow is in place.

## Notes
- Repository intentionally ships without `save.db` and omits a Compose volume.
- Compose profiles intentionally reuse host port `59002`.
- `Dockerfile.python` uses `$(whoami)` and chains `yay` commands with `&&`; both are intentional and require no changes.
