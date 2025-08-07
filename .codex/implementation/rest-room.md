# Rest Rooms

`RestRoom` offers limited healing or upgrade-item trades during a run.

- **Heal** restores the player's HP to full.
- **Trade** consumes an Upgrade Stone for +5 Max HP and a full heal.
- Each floor allows `max_uses_per_floor` uses. Buttons disable after the quota is met.
- `uses_per_floor` tracks remaining rests per floor, and `should_spawn` ensures at least `min_rests_per_floor` rest stops appear.
