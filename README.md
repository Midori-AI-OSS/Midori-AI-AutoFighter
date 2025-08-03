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

## Headless Execution
To run without a display or audio device (e.g., in CI), set dummy SDL drivers:

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy uv run main.py
```

These variables must be provided for every invocation; forgetting them results in `pygame.error: mixer not initialized`.

If audio isn't required, disable the mixer after initializing Pygame:

```python
import pygame
pygame.mixer.quit()
```

This prevents the mixer from accessing sound hardware and avoids the above error when dummy drivers are missing.

Example for GitHub Actions:

```yaml
- run: uv run main.py
  env:
    SDL_VIDEODRIVER: dummy
    SDL_AUDIODRIVER: dummy
```

## Game Workflow
1. At startup, `PluginLoader` scans `plugins/` and restores fighters from `lives/<name>.dat`. These save files are pickled versions of each fighter's state.
2. Before each wave begins, fighters level up and their updated data is written back to the `lives/` folder for persistence.
3. A wave of foes spawns, combining adjectives and themed names before receiving stat bonuses from `foe_passive_builder.py`.
4. Combat plays out automatically while experience and levels accrue. During play, summaries append to `logs/<name>.txt`.
5. When a fighter's HP hits zero, `save_past_life` archives their data to `past_lives/<uuid>.pastlife` and removes the active save.
6. The run concludes after all fighters fall. The engine writes each fighter's final state to `lives/<name>.dat` (e.g., `lives/Ally.dat`) and exits. Saving occurs even if you close the window manually. Restarting the game loads surviving fighters from `lives/`.

### Save Files and Logs
Player progress uses Python's pickle serialization:

```text
lives/Ally.dat   # active save
logs/Ally.txt    # combat history
past_lives/<uuid>.pastlife  # archived runs
```

For a deeper walkthrough, see `.codex/implementation/game-workflow.md`.

## Playable Characters
The roster in `plugins/players/` currently includes:

- Ally
- Becca
- Bubbles
- Carly
- Chibi
- Graygray
- Hilander
- Kboshi
- Lady Darkness
- Lady Echo
- Lady Fire and Ice
- Lady Light
- Lady of Fire
- Luna
- Mezzy
- Mimic

## Enemies
Foes are procedurally named by pairing adjectives and themed names from `themedstuff.py`.

Each adjective and name contributes unique stat bonuses in `foe_passive_builder.py`. For example, **Atrocious Luna** gains dodge and defense from the "Luna" portion while "Atrocious" adds extra attack power. High-level foes whose names start with "Lady" receive large multipliers tied to their theme (Light, Dark, Fire, or Ice).

For a roster breakdown and details on how those modifiers work, see `.codex/implementation/player-foe-reference.md`.

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

