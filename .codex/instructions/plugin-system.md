# Plugin System

The game supports dynamic extensions loaded from the `plugins/` and `mods/`
directories at start-up. The `PluginLoader` traverses these directories and
imports Python modules with plugin classes.

## Directory Layout
```
plugins/
├── players/       # Player implementations
├── foes/          # Enemy implementations
├── passives/      # Passive abilities
├── dots/          # Damage-over-time effects
├── hots/          # Healing-over-time effects
├── weapons/       # Weapon behaviours
├── rooms/         # Room scenes
└── templates/     # Boilerplate files for new plugins
```

## Plugin Classes
Each plugin module should define one or more classes with:

- `plugin_type`: category string such as `player`, `passive`, `dot`, `hot`, or
  `weapon`.
- `id`: unique identifier used by the game. If omitted, the class name becomes
  the identifier.
- Required lifecycle methods like `build`, `apply`, `tick`, or `attack` depending
  on the category.

Modules that fail to import are skipped so a broken plugin does not stop the
discovery process.
 
## Event Bus
Plugins communicate through `EventBus`, which wraps Panda3D's `messenger`:

```
from plugins.event_bus import EventBus

bus = EventBus()
bus.subscribe("my-event", handler)
bus.emit("my-event", data)
```

## Loader Usage
```
from plugins.plugin_loader import PluginLoader

loader = PluginLoader(bus)
loader.discover("plugins")
loader.discover("mods")
players = loader.get_plugins("player")
```

When a bus is supplied, the loader assigns it to a `bus` attribute on each
registered plugin class.

Templates in `plugins/templates/` provide starting points for new plugins.
