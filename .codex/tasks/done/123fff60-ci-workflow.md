# Continuous Integration Workflow

## Summary
Establish a GitHub Actions workflow to run tests on every push and pull request.

## Tasks
- [x] Add `.github/workflows/tests.yml` that installs `uv`, sets up the environment, and executes `uv run pytest`.
- [x] Configure workflow triggers for `push` and `pull_request` events.
- [x] Document the workflow in the README or `.codex/implementation/` to guide contributors.

## Context
The repository lacks continuous integration, so failing tests may go unnoticed.

## Testing
- [x] Submit a pull request to confirm the workflow runs and reports test results.
