# Midori AI AutoFighter

Midori AI AutoFighter is a Pygame-based arena where your fighters clash with endless waves of foes. Characters act automatically while you watch progression unfold.

## Objective and Progression
Survive as long as possible against escalating enemy waves. Defeating foes grants experience and levels that boost your team's stats. Fighters also carry bonus stats from past lives, giving them a growing edge. Enraged foes appear over time, pushing you to keep growing stronger.

## Controls
- **D** – trigger a quick defeat (debugging).
- **B** – grant enemies a temporary attack boost (debugging).
- **Space** – randomize the player's damage type when the fighter is named `player`.
- Close the window or press the system quit button to exit.

## Setup
1. Install [uv](https://github.com/astral-sh/uv).
2. Launch the game (uv automatically prepares the environment and installs dependencies):

   ```bash
   uv run main.py
   ```

## Plugins
Extend the game by dropping Python modules into the `plugins/` folder. The
`PluginLoader` scans subdirectories and registers classes that declare a
`plugin_type` attribute.

```
plugins/
├── players/       # Player implementations
├── passives/      # Passive abilities
├── dots/          # Damage-over-time effects
├── hots/          # Healing-over-time effects
├── weapons/       # Weapon behaviours
└── templates/     # Boilerplate files for new plugins
```

Each plugin module must provide the fields and methods expected for its
category. Custom plugins are detected at startup, letting you tailor fighters,
abilities, and equipment.

## Testing
Run the test suite before submitting changes:

```bash
uv run pytest
```

## Continuous Integration
Tests run automatically on GitHub Actions for each push and pull request (see `.github/workflows/tests.yml`).

## Contributing
1. Fork the repository and create your changes.
2. Follow the commit format `[TYPE] Title`.
3. Ensure tests pass before submitting.
4. Open a pull request describing your changes and any testing performed.

