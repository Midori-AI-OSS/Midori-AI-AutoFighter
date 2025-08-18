// Music loader for background tracks
// Tracks are provided by the lead developer in ./assets/music

const musicModules = import.meta.glob('./assets/music/*', {
  eager: true,
  as: 'url'
});

export function getMusicTracks() {
  return Object.values(musicModules);
}

export function getRandomMusicTrack() {
  const tracks = getMusicTracks();
  if (tracks.length === 0) return '';
  const index = Math.floor(Math.random() * tracks.length);
  return tracks[index];
}
