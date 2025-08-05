# Gacha Pity System

Describes how pity counters raise probabilities for five- and six-star character pulls.

## Pity counters
- `pity_5` counts pulls since the last 5★ character.
- `pity_6` counts pulls since the last 6★ character.

Counters persist via `GachaSystem.serialize()` and `GachaSystem.deserialize()`.

## Probability scaling
- 5★ chance starts at 0.1% and increases by 0.031% per pull.
  - At 179 pulls without a 5★, the next pull is guaranteed.
- 6★ chance starts at 0.01% and increases by 0.0005% per pull.
  - Guaranteed after 2000 pulls.

A single random roll decides the outcome each pull. 6★ is checked first, then 5★. When a character is won:

- 6★ drop resets both counters.
- 5★ drop resets `pity_5` and increments `pity_6`.

Failed pulls increment both counters.

