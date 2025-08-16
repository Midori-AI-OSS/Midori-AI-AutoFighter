# Web Rewrite Task Order

## Summary
Ordered steps for moving Midori AI AutoFighter to a Svelte frontend and a Python Quart backend. Tasks now reflect pronoun limits, damage-type rules, rest-node gacha access, and the decision to drop left-side party and stat viewers in favor of a larger game window. Reminder: list only task titles and file names—open each task file for details. (ready for audit)

- Read `.codex/planning/8a7d9c1e-web-game-plan.md` before starting or auditing any task.
- Coordinate with the reviewer or Task Master before marking a task complete.
- Keep `myunderstanding.md` up to date with the game's flow.

## Tasks
### To Do

### Completed
 - [x] [Fix map orientation and room states](done/ee812dae-fix-map-orientation.md) (`ee812dae`)
 - [x] [Fix navigation buttons](done/f59f2c94-fix-menu-buttons.md) (`f59f2c94`)
 - [x] [Verify unified room action route](done/fd1f6ffd-unified-room-route.md) (`fd1f6ffd`)
 - [x] [Expand game viewport to 95% and remove side viewers](done/2e26511f-expand-game-viewport.md) (`2e26511f`)
 - [x] [Refactor desktop layout with right sidebar](done/41c342ac-desktop-ui-sidebar-refactor.md) (`41c342ac`)
 - [x] [Rebuild settings panel with framerate and autocraft](done/2a4db820-settings-panel-overhaul.md) (`2a4db820`)
 - [x] [Fix menu-induced viewport scaling](done/a449cc04-fix-viewport-bug.md) (`a449cc04`)
 - [x] [Align settings menu with spec](done/985b08e7-settings-layout-fix.md) (`985b08e7`)
 - [x] [Implement crafting menu](done/b3912ca1-crafting-menu.md) (`b3912ca1`)
 - [x] [Hook up pulls menu](done/c6639587-pulls-menu-hookup.md) (`c6639587`)
 - [x] [Hook run button to floor map](done/fb16ba6b-run-button-map.md) (`fb16ba6b`)
 - [x] [Enable map menu navigation](done/cc6b580b-map-menu-access.md) (`cc6b580b`)
 - [x] [Add character editor menu](done/8b6dbc41-character-editor-menu.md) (`8b6dbc41`)
 - [x] [Build gacha character recruitment](done/4d680dc8-gacha-recruitment.md) (`4d680dc8`)
 - [x] [Integrate passive plugin system](done/822626e9-passive-system.md) (`822626e9`)
 - [x] [Build map generator and room types](done/9767b3f3-map-generator-and-rooms.md) (`9767b3f3`)
 - [x] [Implement encrypted save system](done/4b003150-encrypted-save-system.md) (`4b003150`)
 - [x] [Replace legacy player plugin imports](done/f1245ae6-fix-plugin-imports.md) (`f1245ae6`)
 - [x] [Implement room endpoints with game logic](done/541be07f-room-endpoints.md) (`541be07f`)
 - [x] [Remove remaining Panda3D references](done/735b854e-remove-panda3d.md) (`735b854e`)
 - [x] [Expose battle, shop, and rest endpoints](done/b0755eeb-room-endpoints.md) (`b0755eeb`)
 - [x] [Scaffold Quart backend](done/1faf53ba-quart-backend-scaffold.md) (`1faf53ba`)
 - [x] [Add backend tests for run and rooms](5cc4df14-backend-tests.md) (`5cc4df14`)
 - [x] [Fix backend Dockerfile](done/34f8a5b0-fix-backend-dockerfile.md) (`34f8a5b0`)
 - [x] [Add Docker Compose profiles for LLM extras](e09f282f-compose-llm-profiles.md) (`e09f282f`)
 - [x] [Provide player stat screen endpoint](done/9a1c88c4-stat-screen-endpoint.md) (`9a1c88c4`)
 - [x] [Track shop purchases in shared party inventory](done/df5abccd-shop-inventory-tracking.md) (`df5abccd`)
 - [x] [Implement card reward system](done/c7fd49f5-card-reward-system.md) (`c7fd49f5`)
 - [x] [Implement relic system](done/388bd733-relic-system.md) (`388bd733`)
 - [x] [Persist random damage types](done/28c2b708-persist-damage-types.md) (`28c2b708`)
 - [x] [Add party picker endpoint for run setup](done/5ddc2157-party-picker-endpoint.md) (`5ddc2157`)
 - [x] [Add player character editor endpoint](done/6d267bac-player-character-editor-endpoint.md) (`6d267bac`)
 - [x] [Lock player stat editing during runs](done/1c7a29fa-lock-stat-editing.md) (`1c7a29fa`)
 - [x] [Document battle endpoint payload](done/f74d328b-document-battle-payload.md) (`f74d328b`)
 - [x] [Send room selection to backend battle endpoint](done/8c01491a-room-click-backend.md) (`8c01491a`)
 - [x] [Wire start run button to backend](done/d10d985e-start-run-endpoint.md) (`d10d985e`)
 - [x] [Loop battles and process status effects](done/31c94023-battle-loop-effects.md) (`31c94023`)
 - [x] [Make battle loop async-friendly](done/2d3f9ae1-async-battle-await.md) (`2d3f9ae1`)
 - [x] [Apply DoT chance with effect stats and emit combat events](done/9d6d4b7a-effect-hit-resist-dot.md) (`9d6d4b7a`)
- [x] [Add voice setting to audio options](done/6cc0b67f-add-voice-setting.md) (`6cc0b67f`)
- [x] [Lock menus during active battles](done/38560441-battle-lock-ui.md) (`38560441`)
- [x] [Theme start and cancel buttons](done/80ac2de0-theme-start-run-button.md) (`80ac2de0`)
- [x] [Fix navigation buttons](done/f59f2c94-fix-menu-buttons.md) (`f59f2c94`)

 - [x] [Organize asset icon folders](done/1d6c6f08-asset-icon-structure.md) (`1d6c6f08`)
 - [x] [Build reward overlay](done/1457ed34-reward-overlay.md) (`1457ed34`)
## Context
Switching from Panda3D to a web-based GUI with a Quart backend managed via Docker Compose.

## Task Master Notes
- Persistent save database is intentionally omitted; do not ship `save.db` or add a volume.
- `Dockerfile.python` chains `yay` commands with `&&`; this is required and needs no further task.
- Compose profiles should continue sharing host port `59002` to prevent simultaneous use.
