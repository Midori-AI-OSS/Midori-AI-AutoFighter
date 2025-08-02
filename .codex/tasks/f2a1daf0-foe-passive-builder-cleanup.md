# Foe Passive Builder Cleanup

## Summary
Refactor `buldfoepassives.py` into a maintainable module with smaller, well-named helpers.

## Tasks
- [ ] Rename `buldfoepassives.py` to `foe_passive_builder.py`.
- [ ] Break `build_foe_stats` into thematic helper functions grouped by enemy traits.
- [ ] Replace large conditional blocks with data-driven lookups or plugins where practical.
- [ ] Add docstrings and type hints for all new helpers.

## Context
`buldfoepassives.py` is extremely long, poorly named, and relies on hard-coded conditionals that hinder maintainability.

## Testing
- [ ] Run `uv run pytest` to ensure refactored logic maintains expected behavior.
