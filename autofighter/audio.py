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

try:
    from direct.interval.IntervalGlobal import Func
    from direct.interval.IntervalGlobal import Parallel
    from direct.interval.IntervalGlobal import Sequence
    from direct.interval.IntervalGlobal import SoundInterval
except Exception:  # pragma: no cover - Panda3D not available during tests
    class SoundInterval:  # type: ignore[dead-code]
        def __init__(self, sound, *, duration: float = 0.0, volume: float = 1.0) -> None:
            self.sound = sound
            self.volume = volume

        def start(self) -> None:
            self.sound.setVolume(self.volume)

    class Func:  # type: ignore[dead-code]
        def __init__(self, func, *args, **kwargs) -> None:
            self.func = func
            self.args = args
            self.kwargs = kwargs

        def start(self) -> None:
            self.func(*self.args, **self.kwargs)

    class Parallel:  # type: ignore[dead-code]
        def __init__(self, *intervals) -> None:
            self.intervals = intervals

        def start(self) -> None:
            for interval in self.intervals:
                interval.start()

    class Sequence:  # type: ignore[dead-code]
        def __init__(self, *intervals) -> None:
            self.intervals = intervals

        def start(self) -> None:
            for interval in self.intervals:
                interval.start()

from autofighter.assets.manager import AssetManager

class AudioManager:
    """Load and play music and sound effects with volume control."""

    def __init__(self, assets: AssetManager) -> None:
        self.assets = assets
        self.music: AudioSound | None = None
        self.sfx: list[AudioSound] = []
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        self._music_interval: Sequence | None = None

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
        self._music_interval = None

    def crossfade_music(
        self, name: str, duration: float = 1.0, loop: bool = True
    ) -> AudioSound:
        new_sound: AudioSound = self.assets.load("audio", name)
        new_sound.setLoop(loop)
        new_sound.setVolume(0)
        new_sound.play()
        old_sound = self.music
        self.music = new_sound
        if old_sound is None:
            new_sound.setVolume(self.music_volume)
            return new_sound
        fade_out = SoundInterval(old_sound, duration=duration, volume=0)
        fade_in = SoundInterval(new_sound, duration=duration, volume=self.music_volume)
        self._music_interval = Sequence(
            Parallel(fade_out, fade_in),
            Func(old_sound.stop),
        )
        self._music_interval.start()
        return new_sound

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
