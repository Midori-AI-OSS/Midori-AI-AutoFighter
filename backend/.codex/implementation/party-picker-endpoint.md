# Party Picker Endpoint

`POST /run/start` accepts a JSON payload with a `party` array of 1–5 owned character IDs (including `player`) and an optional `damage_type` for the player chosen from Light, Dark, Wind, Lightning, Fire, or Ice.
The backend validates the roster, persists the player's damage type, seeds a new map, and returns the run ID, map data, and passive names for each party member.

## Testing
- `uv run pytest backend/tests/test_party_endpoint.py`
