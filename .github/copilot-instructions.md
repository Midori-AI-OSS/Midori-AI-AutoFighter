# Stained Glass Odyssey: Endless Development Instructions

Always follow this file first, then apply repository and mode-specific `AGENTS.md` guidance.

## Mandatory Preflight
Before starting work:
1. Read this file.
2. Read the nearest applicable `AGENTS.md`.
3. Read your active mode guide in `.agents/modes/`.

## Repository Overview
Stained Glass Odyssey: Endless is a web-based autobattler with:
- `backend/` - Python Quart backend
- `frontend/` - Svelte frontend
- `.agents/` - contributor process docs

## Required Tooling
- Python commands: use `uv` only.
- Node/frontend commands: use `bun` only.
- Do not use `pip` or `npm` directly.

## Core Development Commands
### Backend
```bash
cd backend
uv run app.py
```
Expected: backend on `http://localhost:59002`.

### Frontend
```bash
cd frontend
bun run dev
```
Expected: frontend on `http://localhost:59001`.

### Frontend build
```bash
cd frontend
bun run build
```

## Verification Policy (Hard Rule)
After work, run and report all of the following:

```bash
uv tool run ruff check backend
cd frontend && bun run lint
uvx basedpyright backend
cd backend && uv run pytest tests --collect-only -q
cd backend && uv run python -m compileall .
```

Rules:
- Running these commands is mandatory.
- Passing all checks is preferred but not required to report completion.
- Any failures must be documented in `/tmp/agents-artifacts/agent-output.md` and PR summary.

## Validation Scenarios
When relevant to your change, verify:
1. Backend API health:
```bash
curl http://localhost:59002/
```
Expected: `{"flavor":"default","status":"ok"}`

2. Frontend lint runs successfully (`cd frontend && bun run lint`) when frontend files are touched.

## Known Limitations
- Docker compose builds may fail in this environment due to DNS/network constraints.
- Built executables may hit plugin discovery issues.
- Active development can include pre-existing test/type/lint failures.

## CI Notes
- Backend lint in CI: `uvx ruff check backend`
- Frontend lint in CI: `bunx eslint .`

## Structure Reference
### Key backend files
- `backend/app.py`
- `backend/routes/`
- `backend/autofighter/`

### Key frontend files
- `frontend/src/`
- `frontend/static/`

### Key config
- `backend/pyproject.toml`
- `frontend/package.json`
- `ruff.toml`
- `compose.yaml`
