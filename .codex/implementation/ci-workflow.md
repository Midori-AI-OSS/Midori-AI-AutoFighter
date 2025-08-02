# Continuous Integration Workflow

A GitHub Actions workflow runs the test suite on each push and pull request.

The workflow is defined in `.github/workflows/tests.yml` and uses
[`astral-sh/setup-uv`](https://github.com/astral-sh/setup-uv) to install `uv`
with Python 3.11. It then executes `uv run pytest` to validate the project.
