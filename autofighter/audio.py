from __future__ import annotations

try:
    from panda3d.core import AudioSound
except Exception:  # pragma: no cover - Panda3D not available during tests
    class AudioSound:  # type: ignore[dead-code]
        def __init__(self) -> None:
            self._loop = False
            self._volume = 1.0
            self.playing = False

        def setLoop(self, loop: bool) -> None:  # noqa: N802 - Panda3D style
            self._loop = loop

        def setVolume(self, volume: float) -> None:  # noqa: N802 - Panda3D style
            self._volume = volume

        def play(self) -> None:
            self.playing = True

        def stop(self) -> None:
            self.playing = False

from autofighter.assets.manager import AssetManager

class AudioManager:
    """Load and play music and sound effects with volume control."""

    def __init__(self, assets: AssetManager) -> None:
        self.assets = assets
        self.music: AudioSound | None = None
        self.sfx: list[AudioSound] = []
        self.music_volume = 0.5
        self.sfx_volume = 0.5

    def set_music_volume(self, volume: float) -> None:
        self.music_volume = volume
        if self.music is not None:
            self.music.setVolume(volume)

    def set_sfx_volume(self, volume: float) -> None:
        self.sfx_volume = volume
        for sound in self.sfx:
            sound.setVolume(volume)

    def play_music(self, name: str, loop: bool = True) -> AudioSound:
        sound: AudioSound = self.assets.load("audio", name)
        sound.setLoop(loop)
        sound.setVolume(self.music_volume)
        sound.play()
        self.music = sound
        return sound

    def stop_music(self) -> None:
        if self.music is not None:
            self.music.stop()
            self.music = None

    def play_sfx(self, name: str) -> AudioSound:
        sound: AudioSound = self.assets.load("audio", name)
        sound.setLoop(False)
        sound.setVolume(self.sfx_volume)
        sound.play()
        self.sfx.append(sound)
        return sound

    def stop_sfx(self) -> None:
        for sound in self.sfx:
            sound.stop()
        self.sfx.clear()


_global_audio: AudioManager | None = None


def get_audio() -> AudioManager:
    """Return the global :class:`AudioManager` instance."""

    global _global_audio
    if _global_audio is None:
        _global_audio = AudioManager(AssetManager())
    return _global_audio
