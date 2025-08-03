# Document SDL dummy drivers for headless runs

## Summary
Expand documentation to clearly explain using SDL dummy drivers when running the game without display or sound hardware.

## Details
- In `README.md`, extend the **Headless Execution** section with a paragraph explaining that `SDL_VIDEODRIVER` and `SDL_AUDIODRIVER` must be set to `dummy` before launching `uv run main.py`.
- Show an explicit example command block demonstrating export of both variables on a single line.
- Mention that these variables must be set for every invocation in headless environments.

## Notes
- Based on `.codex/tasks/de1f49f9-headless-audio-doc.md`.
