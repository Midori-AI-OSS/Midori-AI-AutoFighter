# Effect stacking

`EffectManager.maybe_inflict_dot` processes the attacker's `effect_hit_rate` in 100% chunks. Each pass subtracts the target's `effect_resistance` and rolls for a stack using the remaining chance. Additional stacks are only attempted after a successful roll, and the first stack always has at least a 1% chance even when resistance exceeds hit rate.
