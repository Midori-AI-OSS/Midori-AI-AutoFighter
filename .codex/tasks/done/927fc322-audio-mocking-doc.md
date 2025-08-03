# Explain audio disabling to avoid mixer errors

## Summary
Provide guidance on disabling or mocking audio so headless environments do not raise `mixer not initialized` errors.

## Details
- Update `README.md` to show using `SDL_AUDIODRIVER=dummy` to bypass the need for sound hardware.
- Add a troubleshooting note indicating that initializing `pygame.mixer` without an audio device causes the common `mixer not initialized` exception.
- Mention optional approaches such as invoking `pygame.mixer.quit()` if audio is not required.

## Notes
- Based on `.codex/tasks/de1f49f9-headless-audio-doc.md`.
