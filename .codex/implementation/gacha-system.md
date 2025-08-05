# Gacha System

## Duplicate Stacking
- Characters pulled more than once increase their stack count.
- First copy provides no bonus.
- Each duplicate grants Vitality using a geometric series:
  - First duplicate: +0.01% Vitality.
  - Each additional stack adds 5% more than the previous increment.
- Total bonus after *n* stacks is the sum of all increments.
- Stack counts and bonuses persist in `player.json` under a `characters` map.
