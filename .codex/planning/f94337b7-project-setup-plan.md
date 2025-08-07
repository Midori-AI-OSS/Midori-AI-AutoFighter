# Project Setup

1. Move current Pygame code into `legacy/`.
2. Run `uv init` to create a fresh environment.
3. Install Panda3D with `uv add panda3d`; optional LLM extras via `uv add --optional llm`.
   - Include LLM tooling such as `langchain` and Hugging Face `transformers`.
   - Use prebuilt Panda3D wheels; focus build notes on LangChain/transformers for NVIDIA, Intel/AMD GPU, and CPU-only setups.
4. Add `main.py` launching `ShowBase` and rendering a placeholder cube to verify the engine.
5. Scaffold `assets/` (`models/`, `textures/`, `audio/`), `plugins/`, `mods/`, and user-managed `llms/` directories and document the structure in `README.md`.
   - Include player photos with fallback images for missing or failed loads.
6. Update `README.md` to warn contributors not to modify `legacy/` and show how to install the latest code via `uv add git+https://github.com/Midori-AI/Midori-AI-AutoFighter@main`.
7. Commit minimal setup once `main.py` runs.
8. Define a `pyproject.toml` package named `autofighter` and expose an entry point for `main.py`.
   - Research publishing `autofighter` to PyPI once stable; expect moderate effort due to native dependencies and asset management.
9. Ensure `game/__init__.py` initializes the package so imports work.
