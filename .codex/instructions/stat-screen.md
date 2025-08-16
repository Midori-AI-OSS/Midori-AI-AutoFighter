# Stat Screen

The Stat Screen scene displays grouped combat statistics and active effects.

## Categories
- **Core:** HP, Max HP, EXP, Level, EXP multiplier, and actions per turn.
- **Offense:** Attack, crit rate, crit damage, effect hit rate, base damage type.
- **Defense:** Defense, mitigation, regain, dodge odds, effect resistance.
- **Vitality & Advanced:** Vitality, action points, cumulative damage taken/dealt, and kills.
- **Status:** Active passives, DoTs, HoTs, damage types, and relic stacks.

### DoTs
- Bleed – deals 2% of Max HP each turn.
- Celestial Atrophy – reduces Attack every tick.
- Abyssal Corruption – dark damage placeholder.
- Abyssal Weakness – lowers Defense while active.
- Gale Erosion – strips Mitigation each tick.
- Charged Decay – stuns on the final tick.
- Frozen Wound – reduces Actions per Turn.
- Blazing Torment – gains an extra tick whenever the target acts.
- Cold Wound – stacks up to five times.
- Twilight Decay – drains Vitality per tick.
- Impact Echo – repeats 50% of the last hit for three turns.

### HoTs
- Regeneration – heals a flat amount each tick.
- PlayerName's Echo – heals 20% of ally damage for a few turns.
- PlayerName's Heal – applies an instant heal and 1% Max HP per turn.

### Damage Types
- Generic
- Light
- Dark
- Wind
- Lightning
- Fire
- Ice

## Refresh Rate
- Updates every 5 frames by default; accepts values from 1–10.
- Configurable via an Options menu slider.

## Status Hooks
- Call `add_status_hook` with a function returning a list of lines to append to the Status section.
