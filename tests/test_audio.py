from __future__ import annotations

from autofighter.audio import AudioManager


class DummySound:
    def __init__(self) -> None:
        self.loop = False
        self.volume = 1.0
        self.played = False
        self.stopped = False

    def setLoop(self, value: bool) -> None:  # noqa: N802 - Panda3D style
        self.loop = value

    def setVolume(self, value: float) -> None:  # noqa: N802 - Panda3D style
        self.volume = value

    def play(self) -> None:
        self.played = True

    def stop(self) -> None:
        self.stopped = True


class DummyAssets:
    def get_audio(self, _name: str) -> DummySound:
        return DummySound()


def test_volume_updates_adjust_playback() -> None:
    assets = DummyAssets()
    audio = AudioManager(assets)

    music = audio.play_music("track")
    assert music.played is True
    audio.set_music_volume(0.2)
    assert music.volume == 0.2

    effect = audio.play_sfx("boom")
    audio.set_sfx_volume(0.3)
    assert effect.volume == 0.3

    audio.stop_music()
    assert audio.music is None
    audio.stop_sfx()
    assert not audio.sfx


def test_crossfade_music_stops_previous_track() -> None:
    assets = DummyAssets()
    audio = AudioManager(assets)

    first = audio.play_music("first")
    assert first.played is True

    second = audio.crossfade_music("second", duration=0.1)
    assert second.played is True
    assert first.stopped is True
    assert first.volume == 0
    assert second.volume == audio.music_volume
    assert audio.music is second
