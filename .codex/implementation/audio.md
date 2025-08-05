# Audio System

Provides global helpers for playing music and sound effects loaded via `AssetManager`.

## Usage
- `play_music(name: str, loop: bool = True)` – load a track from the asset manifest and begin playback. Previous music stops automatically.
- `stop_music()` – halt the current music track.
- `play_sfx(name: str)` – play a one-shot sound effect.
- `stop_sfx()` – stop all sound effects.
- `set_music_volume(value: float)` / `set_sfx_volume(value: float)` – adjust volumes; active sounds update immediately.

Use `get_audio()` to access the shared `AudioManager` instance. The options menu hooks into these setters so slider changes update playback volume.
