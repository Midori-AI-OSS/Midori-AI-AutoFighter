# Plugin System

The game supports dynamic extensions loaded from the `plugins/` directory at
start-up. The `PluginLoader` scans subdirectories and imports Python modules
with plugin classes.

## Directory Layout
```
plugins/
├── players/       # Player implementations
├── passives/      # Passive abilities
├── dots/          # Damage-over-time effects
├── hots/          # Healing-over-time effects
├── weapons/       # Weapon behaviours
└── templates/     # Boilerplate files for new plugins
```

## Plugin Classes
Each plugin module should define one or more classes with:

- `plugin_type`: category string such as `player`, `passive`, `dot`, `hot`, or
  `weapon`.
- `id`: unique identifier used by the game.
- Required lifecycle methods like `build`, `apply`, `tick`, or `attack` depending
  on the category.

## Loader Usage
```
from plugins.plugin_loader import PluginLoader

loader = PluginLoader()
loader.discover("plugins")
players = loader.get_plugins("player")
```

Templates in `plugins/templates/` provide starting points for new plugins.
