<script>
  import { Mic, Music, Radio, Volume2 } from 'lucide-svelte';
  import DotSelector from './DotSelector.svelte';

  // SFX/Voice currently use 0-10 in parent; music is canonical 0-100.
  export let sfxVolume = 5;
  export let musicVolume = 70;
  export let voiceVolume = 5;
  export let musicSource = 'game';
  export let scheduleSave;

  let dotSfx = Math.round(Number(sfxVolume || 0) * 10);
  let dotMusic = Math.max(0, Math.min(100, Math.round(Number(musicVolume || 70))));
  let dotVoice = Math.round(Number(voiceVolume || 0) * 10);

  function normalizeSource(value) {
    return value === 'midoriai_radio' ? 'midoriai_radio' : 'game';
  }

  function clampVolume(value, fallback = 70) {
    const numeric = Number(value);
    if (!Number.isFinite(numeric)) return fallback;
    return Math.max(0, Math.min(100, Math.round(numeric)));
  }

  $: { const v = Math.round(Number(sfxVolume || 0) * 10); if (v !== dotSfx) dotSfx = v; }
  $: { const v = clampVolume(musicVolume, 70); if (v !== dotMusic) dotMusic = v; }
  $: { const v = Math.round(Number(voiceVolume || 0) * 10); if (v !== dotVoice) dotVoice = v; }
  $: {
    const nextSource = normalizeSource(musicSource);
    if (nextSource !== musicSource) {
      musicSource = nextSource;
    }
  }
</script>

<div class="settings-panel">
  <div class="control" title="Choose the active music source.">
    <div class="control-left">
      <span class="label"><Radio /> Music Source</span>
    </div>
    <div class="control-right">
      <label class="select-wrap">
        <span class="sr-only">Music source</span>
        <select
          bind:value={musicSource}
          on:change={() => {
            musicSource = normalizeSource(musicSource);
            scheduleSave();
          }}
        >
          <option value="game">Game Music</option>
          <option value="midoriai_radio">Midori AI Radio</option>
        </select>
      </label>
    </div>
  </div>
  <div class="control" title="Adjust sound effect volume.">
    <div class="control-left">
      <span class="label"><Volume2 /> SFX Volume</span>
    </div>
    <div class="control-right">
      <DotSelector bind:value={dotSfx} on:change={() => { sfxVolume = Math.round(dotSfx / 10); scheduleSave(); }} />
    </div>
  </div>
  <div class="control" title="Adjust background music volume.">
    <div class="control-left">
      <span class="label"><Music /> Music Volume</span>
    </div>
    <div class="control-right">
      <DotSelector bind:value={dotMusic} on:change={() => { musicVolume = clampVolume(dotMusic, 70); scheduleSave(); }} />
    </div>
  </div>
  <div class="control" title="Adjust voice volume.">
    <div class="control-left">
      <span class="label"><Mic /> Voice Volume</span>
    </div>
    <div class="control-right">
      <DotSelector bind:value={dotVoice} on:change={() => { voiceVolume = Math.round(dotVoice / 10); scheduleSave(); }} />
    </div>
  </div>
</div>

<style>
  @import './settings-shared.css';

  .select-wrap select {
    min-width: 9.2rem;
    background: rgba(0, 0, 0, 0.4);
    border: var(--glass-border, 1px solid rgba(255, 255, 255, 0.22));
    color: inherit;
    padding: 0.25rem 0.45rem;
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    margin: -1px;
    padding: 0;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
  }
</style>
