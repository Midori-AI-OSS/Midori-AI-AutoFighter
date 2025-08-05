
# Gacha system

## Presentation flow
- Determine the highest rarity in the pull results.
- Play the video or animation for that rarity unless the player skips.
- After the animation (or immediately if skipped), show a results menu.
  - Single pulls show one item.
  - Multi pulls list all items.
- Allow skipping at any point to jump directly to the results menu.

Adds a basic character pull system seeded from `plugins/players`.

## Features
- 1, 5, or 10 pulls at a time.
- Failed pulls grant generic upgrade items.
- Duplicate characters apply Vitality stacking bonuses.
- Ownership data serializes to JSON for persistence.
