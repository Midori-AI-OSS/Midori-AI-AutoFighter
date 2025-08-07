# Core Architecture

1. Implement a new `ShowBase` subclass from scratch and exclude legacy imports.
2. Convert event logic to Panda3D's `messenger` and `taskMgr` while keeping frame loops light for low-end hardware.
3. Replace Pygame rendering with Panda3D node graphs.
4. Rebuild the plugin loader and APIs so new player, weapon, passive, DoT, and HoT plugins mirror current concepts without reusing legacy code and expose a mod interface.
   - Add tests verifying discovery of modules under `mods/` to catch empty packages.
5. Add a scene manager capable of swapping menus, gameplay states, and overlays.
   - Handle exceptions gracefully and recover from failed scene loads.
6. Organize source under a `game/` package with submodules (`actors/`, `ui/`, `rooms/`, `gacha/`, `saves/`).
7. Define a `Stats` dataclass holding core attributes; share between players and foes.
8. Provide an event bus wrapper for `messenger` so plugins can subscribe and emit without engine imports.
