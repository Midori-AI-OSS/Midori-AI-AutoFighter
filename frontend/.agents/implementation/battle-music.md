# Battle Music

Describes how the frontend selects playlists for combat.

## selectBattleMusic
`selectBattleMusic({ roomType, party, foes })` returns a playlist of music
tracks for the next room transition. When both party and foe data are present,
character-specific playlists are evaluated immediately. Until battler
information arrives, generic fallback tracks continue playing.

- **Boss rooms** (`roomType === 'battle-boss-floor'`)
  - Always returns the boss's `boss` playlist.
  - Playlist loops continuously.
- **Non-boss battles**
  - Collects playlists for every combatant present.
  - Luna's playlist receives weight 3; all others use weight 1.
  - A weighted roll chooses the resulting playlist, favouring Luna when
    present.
- **Fallback**
  - When no character has music, generic library tracks are returned.

The chosen playlist is passed to `startGameMusic` which accepts a track list,
shuffles it, and crossfades from the previous selection. GameViewport tracks
party and foe identifiers so that when fighter data appears or changes, a new
playlist is requested. If `startGameMusic` receives the same playlist again
during scene changes, it simply reapplies volume, allowing the current music to
keep playing until it naturally ends or a new playlist is requested. When
looping, the playlist is reshuffled after each cycle to avoid repetition.
