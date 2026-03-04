# Repository Contributor Guide

This document summarizes common development practices for all services in this repository.

---

## Where to Look for Guidance (Per-Service Layout)
- **`.feedback/`**: Task lists and priorities. *Read only*.
- **`.agents/`** (inside each service directory, for example `WebUI/.agents/`, `Rest-Servers/.agents/`):
  - Use for contributor coordination (modes, notes, implementation docs).
  - Prefer code and docstrings as the source of truth.
- **Never edit files in `.agents/audit/` unless you are in Auditor mode.**
- **`.github/`**: Workflow guidelines and UX standards.
- When entering any folder, check for an `AGENTS.md` file in that folder and read it before starting work there.

---

## Required Preflight (Hard Rule)
Before starting work, contributors must read:
1. `.github/copilot-instructions.md`
2. The nearest applicable `AGENTS.md`
3. Their mode guide in `.agents/modes/`

Skipping preflight is a process violation.

## Agent Run Log (Hard Rule)
All contributor modes must use `/tmp/agents-artifacts/agent-output.md`.

Required behavior:
- Read `/tmp/agents-artifacts/agent-output.md` before starting work.
- Read it again immediately before appending your entry.
- Append one entry per run.
- Create the file if it does not exist.

Each entry must include:
- timestamp
- role/mode
- scope/files
- intent
- actions taken
- results
- blockers/next step

The run log is mandatory and does not replace normal PR/issue communication.

## Development Basics
- Use [`uv`](https://github.com/astral-sh/uv) for Python environments and commands. Do not use `python` or `pip` directly.
- Use [`bun`](https://bun.sh/) for Node/React tooling. Do not use `npm` or `yarn`.
- Verification-first: confirm current behavior before changing code; then verify the result with clear checks.
- No broad fallbacks: add narrow fallbacks only when explicitly required by the task.
- No compatibility shims by default.
- Minimal docs/logging: prefer code and docstrings over long-form documentation.
- Do not update `README.md`.
- Split large modules when practical.
- If coding in Python, keep async behavior safe (avoid blocking the event loop; use async/await for I/O).
- Python style:
  - One import per line.
  - Sort imports shortest-to-longest within each group.
  - Group order: standard library, third-party, project modules.
  - Insert one blank line between groups.
  - Avoid inline imports.

## Post-Work Verification (Hard Rule)
After completing work, run and report all of the following:

```bash
uv tool run ruff check backend
cd frontend && bun run lint
uvx basedpyright backend
cd backend && uv run pytest tests --collect-only -q
cd backend && uv run python -m compileall .
```

Rules:
- Running the checks is mandatory.
- Passing every check is preferred but not required to report completion.
- Any failures must be reported clearly in the run log and PR summary.

## UI / UX Standards (Hard Rules)
- Preserve the established product visual language and interaction patterns unless the Lead Developer explicitly approves a visual-system change.
- Reuse shared primitives before creating new local UI styles or components.
- Before adding new UI patterns, search for an existing reusable component/style/token and use it when possible.
- Accessibility requirements are mandatory (keyboard flow, semantic labels, focus visibility).
- Reduced-motion behavior is mandatory when motion exists.
- Avoid drive-by visual redesigns in unrelated tasks.

## File Size and Readability
- Aim for about 300 lines or fewer per file.
- Split monolithic files when practical.
- Keep code organized and readable.

---

## Commit and Pull Request Workflow
Follow this checklist whenever you are ready to publish work:

1. Stage and review your changes locally (`git status`, `git diff`).
2. Create a descriptive commit with a `[TYPE]` prefix.
3. Verify the working tree is clean after committing (`git status`).
4. Immediately call the `make_pr` tool to draft PR title/summary after the commit.
5. Never call `make_pr` before committing, and do not finish committed work without a PR draft.
6. If you did not modify the repository, do not commit and do not call `make_pr`.

These steps apply to all contributor modes.

---

## Contributor Modes
The repository supports these contributor modes:

> **MANDATORY:** All contributors must read their mode documentation in `.agents/modes/` before starting work.

- **Manager Mode** (`.agents/modes/MANAGER.md`)
- **Coder Mode** (`.agents/modes/CODER.md`)
- **Reviewer Mode** (`.agents/modes/REVIEWER.md`)
- **Auditor Mode** (`.agents/modes/AUDITOR.md`)
- **QA Mode** (`.agents/modes/QA.md`)
- **Storyteller Mode** (`.agents/modes/STORYTELLER.md`)
- **Unknown Mode** (no file)

All contributors should keep their mode cheat sheet in `.agents/notes/` current.

### Documentation Sync
Prefer code and docstrings as the canonical source; keep notes minimal and task-scoped.
