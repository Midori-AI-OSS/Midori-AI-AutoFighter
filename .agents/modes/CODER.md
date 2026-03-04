# Coder Mode

> **Note:** Prefer the codebase and docstrings as the source of truth. Keep notes minimal and task-scoped.

## Purpose
For contributors actively writing, refactoring, or reviewing code. Coder Mode emphasizes high-quality, maintainable contributions that are easy for others to understand and build upon.

## Guidelines
- Follow all repository coding standards, style guides, and best practices.
- **Recommended**: Run linting before every commit. For backend Python code: `ruff check . --fix` and address any remaining issues manually.
- Write clear, maintainable, and well-structured code with meaningful names.
- Add or update tests for all changes; ensure high test coverage and passing tests.
- Re-run only the tests affected by your change. Use `run-tests.sh` conventions as baseline and scope by impact.
- Use the recommended tools (`uv` for Python, `bun` for Node/React) for consistency and reproducibility.
- Verification-first: confirm current behavior before changing code; verify the fix with clear checks.
- Keep docstrings accurate; avoid creating long-lived documentation artifacts unless explicitly requested.
- Break down large changes into smaller, reviewable commits or pull requests.
- Review your own code before submitting for review.
- **Never edit audit or planning files (see Prohibited Actions below).**
- Ignore time limits; finish the task completely.

## Typical Actions
- Implement new features or enhancements
- Fix bugs or technical debt
- Refactor modules for clarity, performance, or maintainability
- Write or update tests
- Run focused lint/test verification

## Prohibited Actions
**Do NOT edit audit or planning files.**
- Never modify files in `.feedback/`, `.agents/audit/`, `.agents/planning`, or `.agents/review` (or any other audit/planning directories).
- If a planning or audit update is needed, raise it in the pull request or issue discussion instead of editing those directories directly.

## Communication
- Announce start, progress, and completion in pull request updates or linked issue comments.
- Clearly describe purpose and context in commit messages and pull requests.
- Reference related issues, documentation, or discussions when relevant.
