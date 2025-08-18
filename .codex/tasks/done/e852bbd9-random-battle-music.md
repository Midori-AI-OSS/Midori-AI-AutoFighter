# Randomize game music with volume checks (`e852bbd9`)

## Summary
Fights currently lack music. Play background music continuously, choosing a random track on start and whenever one ends while honoring the Settings menu's music volume, updating every ~0.5s.

## Tasks
- [x] Add `static/music/` directory and loader to gather available tracks.
- [x] On viewport mount, pick a random track and play via HTMLAudioElement.
- [x] When a track finishes, automatically start another random track.
- [x] Poll or listen for `musicVolume` changes and adjust playback volume at least twice per second.
- [x] Document audio behavior and mention headless test considerations.

## Context
Users requested continuous background music and volume control integration.

Status: Need Review
