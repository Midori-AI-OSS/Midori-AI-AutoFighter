# Stats and Effect Handling

Defines shared combat statistics and the manager that applies damage and healing over time.

## Stats Fields
The `Stats` dataclass stores core attributes for both players and foes:

- **Core:** `hp`, `max_hp`, `exp`, `level`, `exp_multiplier`, `actions_per_turn`
- **Offense:** `atk`, `crit_rate`, `crit_damage`, `effect_hit_rate`, `base_damage_type`
- **Defense:** `defense`, `mitigation`, `regain`, `dodge_odds`, `effect_resistance`
- **Vitality & Advanced:** `vitality`, `action_points`, `damage_taken`, `damage_dealt`, `kills`
- **Status Lists:** `passives`, `dots`, `hots`, `damage_types`, `relics`

`base_damage_type` is a `DamageType` plugin instance (default `Generic`) instead of a string, allowing damage hooks.
Characters with random base damage types store their first rolled element in the
save database and reuse it on later loads so elements stay consistent across
sessions.

`apply_damage()` and `apply_healing()` update `hp` and track totals such as `damage_taken` and `last_damage_taken`.

## Modifiers
Stat changes may be applied in two ways:

- **Additive:** direct adjustments to integer fields like `hp`, `atk`, or `defense`.
- **Percentage:** float fields such as `crit_rate`, `crit_damage`, `effect_hit_rate`, `effect_resistance`, `vitality`, and `exp_multiplier` represent percentage modifiers.

Effects and passives mutate these fields directly. Percentage values are expressed as decimals (e.g., `0.05` for +5%).

## EffectManager
`EffectManager` tracks `DamageOverTime` and `HealingOverTime` instances on a `Stats` object.

- `add_dot(effect, max_stacks=None)` – registers a DoT; optional stack caps are enforced.
- `add_hot(effect)` – registers a HoT.
- `tick(others=None)` – advances all effects, applying damage or healing and removing expired ones. DoT names are removed from `stats.dots` when finished. If `others` is provided, effects with `on_death` hooks may spread on target death.
- `on_action()` – triggers `on_action` hooks for effects that react when the target performs an action.

Active effect names are mirrored in the `Stats` lists (`dots`, `hots`) for UI display. Plugins can extend base `DamageOverTime` and `HealingOverTime` classes to implement custom behavior or additional stat modifications.
