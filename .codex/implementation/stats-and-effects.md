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

`apply_damage()` and `apply_healing()` update `hp`, fire damage and healing hooks on the attacker and target damage types, and emit
global `damage_taken`, `damage_dealt`, `heal_received`, and `heal` events on the repository-wide event bus.

## Modifiers
Stat changes may be applied in two ways:

- **Additive:** direct adjustments to integer fields like `hp`, `atk`, or `defense`.
- **Percentage:** float fields such as `crit_rate`, `crit_damage`, `effect_hit_rate`, `effect_resistance`, `vitality`, and `exp_multiplier` represent percentage modifiers.

Effects and passives mutate these fields directly. Percentage values are expressed as decimals (e.g., `0.05` for +5%).

## EffectManager
`EffectManager` tracks `DamageOverTime` and `HealingOverTime` instances on a `Stats` object. Ticks call the target's damage type
hooks so plugins can modify dot damage or hot healing globally. Damage types may also create new DoT effects when they land
attacks via `maybe_inflict_dot`, which rolls the attacker's `effect_hit_rate` against the target's `effect_resistance` before
adding the effect. The difference is clamped to zero and jittered by ±10%, and there is always at least a 1% chance to apply the status.

- `add_dot(effect, max_stacks=None)` – registers a DoT. Effects with the same
  ID stack independently, but a `max_stacks` cap can limit simultaneous copies.
- `add_hot(effect)` – registers a HoT. Healing effects always accumulate and
  tick separately with no inherent stack limit.
- `tick(others=None)` – advances all effects, applying damage or healing and removing expired ones. DoT names are removed from `stats.dots` when finished. If `others` is provided, effects with `on_death` hooks may spread on target death.
- `on_action()` – triggers `on_action` hooks for effects that react when the target performs an action.

Active effect names are mirrored in the `Stats` lists (`dots`, `hots`) for UI display. Plugins can extend base `DamageOverTime` and `HealingOverTime` classes to implement custom behavior or additional stat modifications.
