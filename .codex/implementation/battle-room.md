# Battle Room Escalation

## Pressure Level
- `balance.pressure.stat_multiplier(pressure)` adds 5% enemy stat scaling per level.
- `balance.pressure.mechanic_bonus(pressure)` and `reward_multiplier(pressure)` adjust boss traits and loot.

## Floor Boss Escalation
- `balance.floor_boss.scale_stats` multiplies base values by `100 * stat_multiplier(pressure) * 1.2**loop`.
- `scale_mechanics` grants +10% attack per loop and +5% per pressure level, with an extra action every two loops.
- `scale_rewards` multiplies gold by `(2 + 0.5 * loop)` and `reward_multiplier`, awarding up to five tickets.

These rules keep bosses challenging as loops and pressure rise.
