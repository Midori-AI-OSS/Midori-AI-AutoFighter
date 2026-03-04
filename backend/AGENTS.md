# Backend Contributor Guide

> **MANDATORY:** Before touching files under `backend/`, read `.github/copilot-instructions.md`, the repository `AGENTS.md`, and your mode document in `.agents/modes/`.

---

## Quick Orientation
- Backend is a [Quart](https://quart.palletsprojects.com/) ASGI app rooted at `backend/app.py`.
- Blueprints live under `backend/routes/`.
- Keep endpoints async-friendly and aligned with current background task patterns.
- Use [`uv`](https://github.com/astral-sh/uv) for Python tooling.

## Agent Run Log (Hard Rule)
Use `/tmp/agents-artifacts/agent-output.md` for every run.

Required behavior:
- Read the log before work.
- Read it again before appending.
- Append one entry per run.
- Create the file if missing.

Required fields:
- timestamp
- role/mode
- scope/files
- intent
- actions taken
- results
- blockers/next step

## Development and Verification
- Confirm current backend behavior before modifying code.
- Keep runtime changes async-safe.
- Prefer focused backend tests for iterative work (`uv run pytest backend/tests/...`).
- If backend payloads or state contracts change, verify frontend assumptions and sync related `.agents/implementation/` notes.

## Post-Work Verification (Hard Rule)
Run and report all checks:

```bash
uv tool run ruff check .
uvx basedpyright .
uv run pytest tests --collect-only -q
uv run python -m compileall .
```

Rules:
- Running these commands is mandatory.
- Failing checks do not block reporting completion, but failures must be reported in the run log and PR summary.

## Coordination Notes
- Major model, migration, worker, or lifecycle changes require Lead Developer coordination.
- Backend changes that alter frontend-visible behavior must include UI contract review notes.
