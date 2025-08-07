# Menu Scaling Helper

Menus now scale against a base resolution of 1280×720.  A constant scale
factor keeps widgets the same physical size regardless of window
dimensions so layouts remain stable for testing.  Background images pull
from `assets/textures/backgrounds/` with a white fallback when an image
is missing.

## Testing
- `uv run pytest`
