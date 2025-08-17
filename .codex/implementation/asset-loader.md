# Asset Loader

`assetLoader.js` centralizes character portraits, backgrounds, and damage type assets for the frontend.

- Character portraits are loaded from `frontend/src/lib/assets/characters` with fallbacks when a portrait is missing.
- Backgrounds rotate hourly using a seeded random selector.
- `getElementIcon` and `getElementColor` expose consistent damage type icons and colors for Fire, Ice, Lightning, Light, Dark, Wind, and Generic types.

The loader is shared by the party picker, map display, and battle view so character images and type colors stay in sync across the UI.

## Testing
- `bun test frontend/tests/assetloader.test.js`
