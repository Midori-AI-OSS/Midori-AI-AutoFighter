# Continuous Integration Workflow

A GitHub Actions workflow runs tests and linting on each push and pull request.

The workflow is defined in `.github/workflows/ci.yml` and is split into four parallel jobs for better performance and clearer failure identification:

1. **backend-tests**: Uses [`astral-sh/setup-uv`](https://github.com/astral-sh/setup-uv) to install `uv` with Python 3.12, installs backend dependencies, and executes `uv run pytest`
2. **backend-lint**: Uses `uv` to run `uvx ruff check backend` for Python code linting
3. **frontend-tests**: Uses [`oven-sh/setup-bun`](https://github.com/oven-sh/setup-bun) to install `bun`, installs frontend dependencies, and executes `bun test`
4. **frontend-lint**: Uses `bun` to run `eslint` for JavaScript code linting

This parallel structure allows for faster feedback and easier identification of specific failures.
