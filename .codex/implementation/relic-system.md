# Relic System

Relics grant bonuses for the duration of a run, applying at run start and during battles.
New runs begin without relics or cards.
Each relic is implemented as a plugin under `plugins/relics/`, allowing new relics
to be added without touching core modules. Awarding the same relic multiple times stacks its effects for that run.

## Testing
- `uv run pytest backend/tests/test_relics.py`
