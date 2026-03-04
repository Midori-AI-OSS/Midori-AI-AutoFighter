# Stat modifiers

Temporary buffs or debuffs adjust numeric fields on a `Stats` object.  The
`StatModifier` effect tracks original values so changes can be reverted when the
modifier expires.

Use `create_stat_buff(stats, **changes)` to build a modifier without boilerplate.
Keyword arguments ending with `_mult` multiply the associated stat; other keys
apply additive deltas.  The factory applies the effect immediately and returns
it for registration with an `EffectManager`:

```python
mod = create_stat_buff(target, atk=10, defense_mult=1.5, turns=2)
manager.add_modifier(mod)
```

`EffectManager.tick()` decrements modifier durations alongside damage and
healing effects, removing and restoring stats once turns reach zero.

Player customization applies a long-lived `StatModifier` rather than modifying
baseline stats. The customization parameters are persisted separately so the
effect can be recreated when loading a run.

Effects can also adjust `aggro_modifier` to influence target selection. The
final `aggro` value is computed from `base_aggro`, the accumulated
`aggro_modifier`, and current defense.
