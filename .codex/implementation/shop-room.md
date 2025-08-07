# Shop Room

Offers upgrade items and cards for gold with a reroll option.

- **Stock** – three random items roll from a small pool and display name, star rating, and price. Buttons disable after buying.
- **Reroll** – spending 10 gold refreshes the entire stock.
- **Persistence** – exiting saves remaining gold and acquired items through `save_player`.
- **Spawn rules** – `ShopRoom.should_spawn` ensures at least two shops appear per floor by tracking spawns in `spawns_per_floor`.
