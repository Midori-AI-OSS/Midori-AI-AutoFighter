# Ensure game music respects volume setting (`3a8ad5ea`)

## Summary
Background music ignores the player's volume setting, playing at default loudness regardless of preference.

## Tasks
- [x] Apply saved `musicVolume` when starting and looping tracks.
- [x] Re-sync audio volume with settings changes.
- [x] Update docs to describe volume polling.

## Context
Players report the settings menu's music volume slider has no effect.

Status: Need Review
