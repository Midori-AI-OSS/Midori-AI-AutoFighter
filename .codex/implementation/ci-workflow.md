# Continuous Integration Workflow

A GitHub Actions workflow runs tests and linting on each push and pull request.

The workflow is defined in `.github/workflows/ci.yml` and uses matrix strategies to automatically discover test files and create parallel jobs for maximum granularity and performance:

## Matrix-Based Test Discovery

The workflow automatically discovers test files and creates parallel jobs without requiring manual updates when new tests are added:

### Backend Tests
- **Discovery Job**: `discover-backend-tests` scans `backend/tests/` for files matching `test_*.py`
- **Test Jobs**: `backend-tests` matrix creates one job per discovered test file
- **Environment**: Uses [`astral-sh/setup-uv`](https://github.com/astral-sh/setup-uv) with Python 3.12
- **Command**: `uv run pytest tests/{test-file}` for each discovered file

### Frontend Tests  
- **Discovery Job**: `discover-frontend-tests` scans `frontend/tests/` for files matching `*.test.js`
- **Test Jobs**: `frontend-tests` matrix creates one job per discovered test file
- **Environment**: Uses [`oven-sh/setup-bun`](https://github.com/oven-sh/setup-bun)
- **Command**: `bun test tests/{test-file}` for each discovered file

## Linting Jobs (2 jobs)
- **backend-lint**: Uses `uv` to run `uvx ruff check backend` for Python code linting
- **frontend-lint**: Uses `bun` to run `eslint` for JavaScript code linting

## Benefits of Matrix Approach

🔄 **Auto-Discovery**: New test files are automatically included without workflow changes  
🚀 **Maximum Parallelization**: Each test file runs in its own job (currently 27 backend + 22 frontend = 49 test jobs)  
🎯 **Pinpoint Failure Identification**: Each job provides status for a specific test file  
⚡ **Fastest Possible Feedback**: No waiting for other tests when one fails  
🛠️ **Zero Maintenance**: Adding/removing tests requires no CI workflow updates  

## Current Test Coverage

As of the latest scan:
- **Backend**: 27 test files (`test_*.py` in `backend/tests/`)
- **Frontend**: 22 test files (`*.test.js` in `frontend/tests/`)
- **Total**: 49 parallel test jobs + 2 linting jobs = 51 total jobs

The matrix approach ensures the workflow automatically adapts to changes in the test suite without manual intervention.
