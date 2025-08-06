# Plugin System

Describes how plugins are discovered, categorized, and connected to the event bus.

## Loader Flow
- `PluginLoader` scans each directory recursively for Python files, skipping `__init__.py` and importing the rest【F:plugins/plugin_loader.py†L24-L38】
- After loading, any categories listed as required but missing raise a runtime error【F:plugins/plugin_loader.py†L40-L48】
- Classes defining `plugin_type` are registered under that category and assigned the event bus when provided【F:plugins/plugin_loader.py†L67-L74】

## Plugin Categories
The following categories are bundled:

- **Players** – controllable characters such as `SamplePlayer`【F:plugins/players/sample_player.py†L4-L8】
- **Foes** – enemy combatants such as `SampleFoe`【F:plugins/foes/sample_foe.py†L4-L8】
- **Passives** – always-on effects like `SamplePassive`【F:plugins/passives/sample_passive.py†L4-L8】
- **DoTs** – damage-over-time effects such as `Bleed`【F:plugins/dots/bleed.py†L4-L15】
- **HoTs** – healing-over-time effects such as `Regeneration`【F:plugins/hots/regeneration.py†L4-L9】
- **Weapons** – attack implementations such as `SampleWeapon`【F:plugins/weapons/sample_weapon.py†L4-L8】
- **Rooms** – scene definitions such as `SampleRoom`【F:plugins/rooms/sample_room.py†L1-L3】

## Event Bus Integration
`PluginLoader` assigns an `EventBus` instance to each plugin, letting them emit and subscribe to events without importing Panda3D's messenger directly【F:plugins/event_bus.py†L40-L54】【F:plugins/plugin_loader.py†L67-L74】

## Adding New Plugin Types
1. Create a new subfolder under `plugins/` for the category.
2. Define classes with a unique `plugin_type` string and optional `id`.
3. Call `PluginLoader.discover` on the new directory and access the category via `get_plugins`.
4. Update `required` when constructing `PluginLoader` if the game should fail when the category is missing.

## Responsive Widgets
Plugins that render DirectGUI elements should scale and position them according to the current window.  Helpers in `autofighter.gui` provide normalized coordinates and scale values derived from `base.win.get_size()` and display DPI:

```python
from autofighter.gui import get_normalized_scale_pos

scale, pos = get_normalized_scale_pos(640, 360)
DirectButton(text="OK", scale=scale, pos=pos)
```

This keeps UI consistent across resolutions and helps plugins remain responsive.
