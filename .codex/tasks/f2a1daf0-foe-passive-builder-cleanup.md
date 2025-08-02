# Foe Passive Builder Cleanup

## Summary
Refactor `buldfoepassives.py` into a maintainable module with smaller, well-named helpers.

## Tasks
- [x] Rename `buldfoepassives.py` to `foe_passive_builder.py`.
- [x] Break `build_foe_stats` into thematic helper functions grouped by enemy traits.
- [ ] Replace large conditional blocks with data-driven lookups or plugins where practical.
- [x] Add docstrings and type hints for all new helpers.

## Context
`buldfoepassives.py` is extremely long, poorly named, and relies on hard-coded conditionals that hinder maintainability. The module applies foe passives at runtime and must stay separate from player stat logic in `damagestate.py`.

## Testing
- [x] Run `uv run pytest` to ensure refactored logic maintains expected behavior.
