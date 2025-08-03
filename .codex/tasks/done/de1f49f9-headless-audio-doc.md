# Document headless and audio setup

## Summary
Add instructions for running the game in environments without display or audio, including required environment variables and troubleshooting for `mixer not initialized` errors.

## Details
- Note `SDL_VIDEODRIVER` and `SDL_AUDIODRIVER` usage for headless runs.
- Mention how to disable or mock audio to prevent mixer errors.
- Provide guidance for CI and automated tests.

## Notes
- Source findings from `.codex/reviews/abf8531b-review-note.md`.
