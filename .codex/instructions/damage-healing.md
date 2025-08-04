# Damage and Healing Effects

## Overview
The combat system tracks damage-over-time (DoT) and healing-over-time (HoT) effects
via dataclasses in `autofighter/effects.py`. Plugins under `plugins/dots/` and
`plugins/hots/` implement specific behaviors.

## Supported DoTs
- Bleed – deals 2% of Max HP each turn.
- Celestial Atrophy – reduces Attack every tick.
- Abyssal Corruption – dark damage that spreads to nearby foes when the target falls.
- Abyssal Weakness – lowers Defense while active.
- Gale Erosion – strips Mitigation each tick.
- Charged Decay – stuns on the final tick.
- Frozen Wound – reduces Actions per Turn.
- Blazing Torment – gains an extra tick whenever the target acts.
- Cold Wound – stacks up to five times.
- Twilight Decay – drains Vitality per tick.
- Impact Echo – repeats 50% of the last damage taken for three turns.

## Supported HoTs
- Regeneration – heals a flat amount each tick.
- PlayerName's Echo – heals 20% of ally damage for a few turns.
- PlayerName's Heal – applies an instant heal and 1% Max HP per turn.

## Testing
- Run `uv run pytest` to validate DoT and HoT behaviors.
