# Document headless setup for CI and tests

## Summary
Add clear instructions for configuring continuous integration and automated tests to run the game without display or audio devices.

## Details
- In `.github/workflows/` templates or developer documentation, include environment exports for `SDL_VIDEODRIVER=dummy` and `SDL_AUDIODRIVER=dummy` before any game invocation.
- Provide an example in `README.md` or `.codex/instructions/` showing how to set these variables in shell scripts or CI YAML files.
- Note that failing to set these variables will result in `pygame.error: mixer not initialized` during tests.

## Notes
- Based on `.codex/tasks/de1f49f9-headless-audio-doc.md`.
