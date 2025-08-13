# Stat Screen Endpoint

Returns grouped statistics for the player's avatar.

- **Route** – `GET /player/stats` responds with `stats` and `refresh_rate` fields.
- **Groups** – `core`, `offense`, `defense`, `vitality`, `advanced`, and `status` lists for passives, DoTs, HoTs, and damage types.
- **Status hooks** – Plugins call `add_status_hook` to append extra status lines before the response is sent.
- **Refresh rate** – Reads `stat_refresh_rate` from the `options` table, defaults to `5`, and clamps to the 1–10 range.
- **Testing** – `uv run pytest backend/tests/test_player_stats.py`
