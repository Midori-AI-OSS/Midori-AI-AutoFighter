# Game Music

`GameViewport.svelte` plays background music continuously. On mount it picks a random
track from `src/lib/assets/music` and starts playback through an `HTMLAudioElement`.
Each time a track ends, another random track begins so music persists for the entire
session. The player's `musicVolume` setting is applied when a track starts and polled
from saved settings roughly every 0.5 s so volume changes take effect quickly.

Headless environments may not support audio playback; tests rely on Bun's no-op `Audio`
implementation so CI runs without sound hardware.
