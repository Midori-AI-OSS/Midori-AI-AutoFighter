# Organize Asset Icon Folders

## Summary
Item, relic, and card icons are missing. Set up asset folders with placeholder images for artists.

## Instructions
- Move generic dot icons from `frontend/src/lib/assets/dots/generic` into a new `assets/items/` directory.
- Create seven damage-type subfolders under `assets/items/` and copy the generic icons into each.
- Create `assets/relics/` and `assets/cards/` with subfolders for each star rank plus a `fallback/` folder.
- Resize placeholders to `24x24` and display them in a colored box based on star rarity.

## Context
Prepares the frontend for item, relic, and card art by providing a structured asset layout.
