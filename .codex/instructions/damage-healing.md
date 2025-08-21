# Damage and Healing Effects

## Stats and Modifiers
Combatants use the shared `Stats` dataclass from `autofighter/stats.py`. Integer fields like `hp`, `atk`, and `defense` are adjusted additively, while floats such as `crit_rate`, `crit_damage`, `effect_hit_rate`, `effect_resistance`, `vitality`, and `exp_multiplier` represent percentage modifiers (e.g., `0.05` for +5%).

## Effect Processing
`autofighter/effects.py` defines base `DamageOverTime` and `HealingOverTime` classes and an `EffectManager` that applies them. The manager:
- Registers effects via `add_dot` and `add_hot`, enforcing optional stack caps.
- Calls `tick` each turn to apply damage or healing and remove expired effects. Completed effect names are removed from the target's `Stats` lists.
- Triggers `on_action` hooks when the target acts, letting effects like *Blazing Torment* respond immediately.

Plugins under `plugins/dots/` and `plugins/hots/` subclass the base effect classes to implement specific behaviors.
Lightning damage pops all active DoTs on hit, applying 25% of each effect's damage immediately without reducing remaining turns.

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
