# Panda3D Project Scaffold

## Summary
Set up the initial Panda3D project structure and environment.

## Tasks
- [x] Move existing Pygame code into `legacy/` and keep it read-only.
- [x] Run `uv init` to create a fresh environment.
- [x] Install Panda3D and optional LLM tooling via `uv add panda3d` and `uv add --optional llm`.
- [x] Add `main.py` that launches `ShowBase` and renders a placeholder cube to verify the engine.
- [x] Scaffold directories: `assets/models/`, `assets/textures/`, `assets/audio/`, `plugins/`, `mods/`, and `llms/`.
- [x] Document the new directory structure in `README.md` and warn contributors not to modify `legacy/`.
- [x] Define `pyproject.toml` with package name `autofighter` and expose an entry point for `main.py`.
- [x] Research publishing `autofighter` to PyPI and note considerations for native dependencies.
- [x] Commit minimal setup once `main.py` runs.
- [ ] Document this feature in `.codex/implementation`.
- [ ] Add unit tests covering success and failure cases.

## Context
A clean scaffold establishes the foundation for all future Panda3D development.

## Testing
- [x] Run `uv run pytest`.

status: failed - `main.py` lacks a placeholder model and README skips optional LLM setup and build notes
