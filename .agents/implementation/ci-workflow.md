# Continuous Integration Workflow

GitHub Actions workflows run tests and linting for frontend and backend components separately.

The workflows are defined in separate files to reduce notification spam and provide clear separation of concerns:

## Separate Frontend and Backend CI

### Backend CI (`.github/workflows/backend-ci.yml`)
- **Single Job**: `backend` combines both testing and linting
- **Environment**: Uses [`astral-sh/setup-uv`](https://github.com/astral-sh/setup-uv) with Python 3.12
- **Linting**: `uvx ruff check backend` for Python code linting
- **Testing**: `uv run pytest tests/` runs all backend tests in parallel within pytest

### Frontend CI (`.github/workflows/frontend-ci.yml`)
- **Single Job**: `frontend` combines both testing and linting
- **Environment**: Uses [`oven-sh/setup-bun`](https://github.com/oven-sh/setup-bun)
- **Linting**: `bunx eslint .` for JavaScript code linting 
- **Testing**: `bun test tests/` runs all frontend tests in parallel within bun

## Benefits of Separated Approach

🔇 **Reduced Notification Spam**: Only 2 total jobs instead of 51 individual jobs  
🎯 **Clear Separation**: Frontend and backend failures are isolated  
⚡ **Fast Feedback**: Tests still run in parallel within each test runner  
🛠️ **Simplified Maintenance**: No complex matrix strategies or discovery jobs needed  
🏗️ **Fail Fast**: Linting runs before tests in each workflow  

## Current Test Coverage

As of the latest scan:
- **Backend**: 96 test files (`test_*.py` in `backend/tests/`) - all run together in pytest
- **Frontend**: 28 test files (`*.test.js` in `frontend/tests/`) - all run together in bun test
- **Total**: 2 CI jobs (1 backend, 1 frontend)

Both workflows use `workflow_dispatch` triggers for manual execution.
