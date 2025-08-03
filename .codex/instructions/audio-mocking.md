# Disabling or Mocking Audio

Headless environments lack sound hardware, leading `pygame` to raise `mixer not initialized` if the mixer tries to access audio devices.

## Avoiding mixer errors
- Set `SDL_AUDIODRIVER=dummy` when invoking the game to bypass hardware requirements.
- Alternatively, shut down the mixer after `pygame.init()`:

```python
import pygame
pygame.mixer.quit()
```

Both approaches prevent attempts to use real audio devices during automated tests or CI runs.
