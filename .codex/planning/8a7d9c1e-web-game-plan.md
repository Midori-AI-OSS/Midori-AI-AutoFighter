# Web GUI and Quart Game Plan

## Goal
Transition Midori AI AutoFighter to a web-based architecture. The game's logic remains in Python, served through a Quart server, while the user interface runs in a separate Svelte frontend. The project no longer targets 3D rendering.

Status: run start and map interactions incomplete. (ready for audit)

## Project Lead Feedback
- Use Svelte for the frontend, keeping the main menu's high-contrast icon grid inspired by Arknights.
- Use Lucide or equivalent icons with clear labels and ensure layouts scale across desktop and mobile resolutions.
- Reuse existing plugin-driven combat, menus, stat screens, and multi-room run map.
- Manage the JS frontend and Quart backend with Docker Compose.
- Keep `myunderstanding.md` current with gameplay flow updates.
- On desktop, present three windows: a landscape game viewport on the right, a small party viewer on the left, and a target stats panel that slides over the party viewer when a unit is selected.
- The settings menu must contain three columns (audio, system/gameplay, other) and include 30/60/120 FPS options that govern server polling along with an autocraft toggle.

## Current Issues
- Start Run button returns to main menu instead of starting a run.
- Start Run and Cancel buttons lack stained glass theme.
- Map appears upside down and does not indicate starting room.
- Room buttons do not trigger backend battle requests or remove visited rooms.
- Battle endpoint payload is undocumented.
- Back button returns to the home screen instead of the previous menu.
- Home button does not navigate anywhere.
- Player editor button beside Home is inactive.
- Settings menu is missing a voice option under the audio column.
- Frontend does not check for active backend battles or lock other menus during a fight.
 - Item, relic, and card icons are missing; move generic dots into `assets/items/` with seven damage-type subfolders, add `assets/relics/` and `assets/cards/` with star-rank and `fallback` subfolders, and resize placeholders to 24×24 in colored rarity boxes.


## Immediate Playable Flow
Playable loop is blocked until start-run and map interactions function correctly.

## Detailed Plans
Detailed planning documents will be written once the playable flow is in place.

## Notes
- Repository intentionally ships without `save.db` and omits a Compose volume.
- Compose profiles intentionally reuse host port `59002`.
- `Dockerfile.python` uses `$(whoami)` and chains `yay` commands with `&&`; both are intentional and require no changes.
- The `legacy/` folder contains historical Panda3D code and is not part of the web rewrite.
