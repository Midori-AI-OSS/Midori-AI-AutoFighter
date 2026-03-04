# Player Editor Endpoint

`GET /player/editor` returns saved pronouns, the player's element, and stat
allocations. `PUT /player/editor` accepts a JSON body with `pronouns`,
`damage_type`, `hp`, `attack`, and `defense`. Pronouns are limited to 15
characters, damage type must be one of Light, Dark, Wind, Lightning, Fire, or
Ice, and the three stats cannot exceed 100 total points. Each point adds a 1%
multiplier to the matching base stat (100 points doubles it). Edits now persist
even if a run is active; when a new run begins the current pronouns, damage
type, and stat distribution are snapshot into the run so later edits do not
affect the active session.

These allocations persist as an effect descriptor rather than by mutating the
player's base stats. When a run loads, the saved parameters rebuild a
long-lived `StatModifier` to apply the chosen multipliers.

Additional endpoints `GET /players/<pid>/editor` and `PUT /players/<pid>/editor`
persist stat allocations for any roster character. These calls mirror the
player editor but omit pronouns and damage type. Stats are stored in the save
data under keys like `player_stats_<pid>` so each character maintains its own
allocation record.

## Testing
- `uv run pytest backend/tests/test_player_editor.py`
