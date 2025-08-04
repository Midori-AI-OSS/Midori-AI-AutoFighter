# Panda3D Project Scaffold

## Summary
Set up the initial Panda3D project structure and environment.

## Tasks
- [ ] Move existing Pygame code into `legacy/` and keep it read-only.
- [ ] Run `uv init` to create a fresh environment.
- [ ] Install Panda3D and optional LLM tooling via `uv add panda3d` and `uv add --optional llm`.
- [ ] Add `main.py` that launches `ShowBase` and renders a placeholder cube to verify the engine.
- [ ] Scaffold directories: `assets/models/`, `assets/textures/`, `assets/audio/`, `plugins/`, `mods/`, and `llms/`.
- [ ] Document the new directory structure in `README.md` and warn contributors not to modify `legacy/`.
- [ ] Update `README.md` with installation instructions using `uv add git+https://github.com/Midori-AI/Midori-AI-AutoFighter@main`.
- [ ] Define `pyproject.toml` with package name `autofighter` and expose an entry point for `main.py`.
- [ ] Research publishing `autofighter` to PyPI and note considerations for native dependencies.
- [ ] Commit minimal setup once `main.py` runs.

## Context
A clean scaffold establishes the foundation for all future Panda3D development.

## Testing
- [ ] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.
