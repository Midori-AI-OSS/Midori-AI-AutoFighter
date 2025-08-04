# Testing and CI Integration

## Summary
Establish automated tests and GitHub workflows for the Panda3D remake.

## Tasks
- [ ] Add unit tests for menus, stat screen, map navigation, gacha logic, and data wiring under `tests/`.
- [ ] Configure headless Panda3D fixtures to run in CI.
- [ ] Create a GitHub Actions workflow to run `uv run pytest` and lint on pushes and pull requests.
- [ ] Document how to run tests locally.

## Context
Automated testing ensures stability as the new engine evolves.

## Testing
- [ ] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.
