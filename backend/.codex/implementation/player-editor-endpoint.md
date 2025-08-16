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

## Testing
- `uv run pytest backend/tests/test_player_editor.py`
