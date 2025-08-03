# Headless CI execution

Continuous integration environments lack display and audio hardware.

Set dummy SDL drivers before invoking the game or tests:

```yaml
- run: uv run pytest
  env:
    SDL_VIDEODRIVER: dummy
    SDL_AUDIODRIVER: dummy
```

Use the same pattern for any job that runs `uv run main.py`.

If `pygame` still raises `mixer not initialized`, disable audio entirely after initializing the library:

```python
import pygame
pygame.mixer.quit()
```

This prevents CI runs from attempting to access missing sound hardware.
