
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
- Upgrade items craft automatically: 125 lower-star items form one higher star.
- Ten 4★ items trade for an extra gacha ticket.
- Duplicate characters apply Vitality and stat bonuses. Each stat uses the first
  duplicate's value from the player plugin and increases by 5% per additional
  stack. Characters can stack duplicates endlessly; each extra pull increases
  the stack and grants the corresponding bonuses.
- Ownership data serializes to JSON for persistence.
