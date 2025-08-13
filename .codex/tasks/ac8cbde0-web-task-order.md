# Web Rewrite Task Order

## Summary
Ordered steps for moving Midori AI AutoFighter to a Svelte frontend and a Python Quart backend. Tasks now reflect pronoun limits, damage-type rules, and rest-node gacha access. Reminder: list only task titles and file names—open each task file for details. (ready for audit)

- Read `.codex/planning/8a7d9c1e-web-game-plan.md` before starting or auditing any task.
- Coordinate with the reviewer or Task Master before marking a task complete.
- Keep `myunderstanding.md` up to date with the game's flow.

## Tasks
### To Do
- [ ] [Implement relic system](388bd733-relic-system.md) (`388bd733`)
- [x] [Implement card reward system](done/c7fd49f5-card-reward-system.md) (`c7fd49f5`)
- [ ] [Build gacha character recruitment](4d680dc8-gacha-recruitment.md) (`4d680dc8`)
- [ ] [Add player character editor endpoint](6d267bac-player-character-editor-endpoint.md) (`6d267bac`)
- [ ] [Add party picker endpoint for run setup](5ddc2157-party-picker-endpoint.md) (`5ddc2157`)
- [ ] [Lock player stat editing during runs](1c7a29fa-lock-stat-editing.md) (`1c7a29fa`)
 - [x] [Persist random damage types](done/28c2b708-persist-damage-types.md) (`28c2b708`)

### Completed
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

## Context
Switching from Panda3D to a web-based GUI with a Quart backend managed via Docker Compose.

## Task Master Notes
- Persistent save database is intentionally omitted; do not ship `save.db` or add a volume.
- `Dockerfile.python` chains `yay` commands with `&&`; this is required and needs no further task.
- Compose profiles should continue sharing host port `59002` to prevent simultaneous use.
