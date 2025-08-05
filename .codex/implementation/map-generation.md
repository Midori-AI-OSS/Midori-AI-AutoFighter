# Map Generation and Pressure Scaling

The map generator builds deterministic floor layouts using a seeded
`MapGenerator`. Pressure Level influences both room structure and
combat difficulty.

## Seed Tracking
Base seeds are persisted to `used_seeds.json`. Creating a `MapGenerator`
checks this list and raises a `ValueError` if a seed was used before.
This prevents regenerating identical maps across runs. The storage path
can be overridden with the `seed_store_path` argument for testing or
custom setups.

## Room Adjustments
- Base floors contain 45 rooms.
- Every 10 Pressure Levels add one room before the floor boss.
- Branching paths are introduced every 15 Pressure Levels. Branches
  skip one room ahead and rejoin the main path.
- Extra boss rooms appear at a rate of one per 20 Pressure Levels and
  are placed throughout the floor.

## Enemy Scaling
Enemy stats scale with floor, room, and loop counts. Additional
Pressure Level modifiers are applied via
`autofighter.balance.pressure.apply_pressure` during battle setup.
