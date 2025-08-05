# Gacha System

The gacha system provides random item rolls with a configurable pity mechanic.

## Configuration
- `base_rate`: starting chance of receiving the top reward.
- `pity_start`: number of failed pulls before odds begin to increase.
- `pity_increment`: additional chance applied after each failed pull once pity starts.
- `pity_threshold`: number of failed pulls after which the next pull is guaranteed.

## Persistence
`GachaSystem` exposes `to_dict` and `from_dict` for saving and loading pity state, allowing the counter to persist between sessions.
