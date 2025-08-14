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
None.

## Immediate Playable Flow
Playable loop is in place; future work will expand content and polish.

## Detailed Plans
Detailed planning documents will be written once the playable flow is in place.

## Notes
- Repository intentionally ships without `save.db` and omits a Compose volume.
- Compose profiles intentionally reuse host port `59002`.
- `Dockerfile.python` uses `$(whoami)` and chains `yay` commands with `&&`; both are intentional and require no changes.
- The `legacy/` folder contains historical Panda3D code and is not part of the web rewrite.
