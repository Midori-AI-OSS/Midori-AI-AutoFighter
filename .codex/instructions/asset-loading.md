# Asset Loading

This service’s frontend resolves images purely in the browser using `import.meta.glob`, avoiding Node-only APIs.

- Backgrounds: a random `.png` is selected from `frontend/src/lib/assets/backgrounds` when the viewport initializes.
- Character portraits:
  - If `frontend/src/lib/assets/characters/<name>.png` exists, that file is used.
  - Else, if `frontend/src/lib/assets/characters/<name>/` exists, one `.png` from that folder is picked at random.
  - Else, a random fallback from `frontend/src/lib/assets/characters/fallbacks/` is used. If no fallbacks are present, the Midori AI logo is used as a final fallback.
- Reward cards: grayscale images are gathered from `frontend/src/lib/assets/cards/*/*.png`. `rewardLoader.js` maps card IDs to these files and provides a placeholder from `frontend/src/lib/assets/cards/fallback/` when no match exists. The reward overlay tints each card by star rank using CSS.

Implementation lives in `frontend/src/lib/assetLoader.js` and should remain free of Node imports so Vite/Bun can bundle for the browser without externalization errors.
