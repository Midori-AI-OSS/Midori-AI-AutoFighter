# Rest Rooms

`RestRoom` nodes provide a quiet break where players can recruit new characters,
craft items, and adjust the party before continuing a run.

- **Pull Character** spends gacha currency using the shared pity counter. Any
  recruits join the roster immediately.
- **Switch Party** opens the party picker to swap members without advancing the
  room.
- **Craft** opens the crafting menu for combining materials.
- Each floor allows `max_uses_per_floor` rest actions. Buttons disable after the
  quota is met. `uses_per_floor` tracks remaining rests per floor, and
  `should_spawn` ensures at least `min_rests_per_floor` rest stops appear.

The frontend provides a placeholder `RestRoom` menu built with `MenuPanel` that
displays **Pull Character**, **Switch Party**, and **Craft** buttons.
