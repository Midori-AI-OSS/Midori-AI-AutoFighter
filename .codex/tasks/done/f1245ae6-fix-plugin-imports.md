# Replace Legacy Player Plugin Imports
Update player plugins to remove dependencies on `game.actors` and use current backend modules.

## Requirements
- Refactor imports in `backend/plugins/players/*.py` to valid module paths.
- Confirm backend starts without `ModuleNotFoundError` for `game` modules.

## Acceptance Criteria
- Backend boots successfully with updated plugins.
- Tests cover plugin import paths.
