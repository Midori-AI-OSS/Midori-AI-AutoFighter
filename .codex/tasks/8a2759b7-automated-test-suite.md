# Automated Test Suite

## Summary
Introduce a pytest-based test suite covering core mechanics and plugin discovery.

## Tasks
- [ ] Create a `tests/` package with an empty `__init__.py`.
- [ ] Add tests verifying player initialization and basic combat calculations.
- [ ] Add tests ensuring the plugin loader registers valid modules and skips malformed ones.
- [ ] Update `pyproject.toml` if necessary so `uv run pytest` locates the tests.

## Context
Currently `pytest` reports zero collected items, offering no automated regression coverage.

## Testing
- [ ] Run `uv run pytest` and confirm all tests pass.
