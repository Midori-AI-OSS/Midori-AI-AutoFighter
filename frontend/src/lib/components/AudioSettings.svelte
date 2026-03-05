<script>
  import { onMount } from 'svelte';
  import { Mic, Music, Power, Radio, Signal, Volume2 } from 'lucide-svelte';
  import DotSelector from './DotSelector.svelte';
  import { getRadioChannels, normalizeRadioChannel, normalizeRadioQuality } from '../systems/radioApi.js';

  // Parent uses 0–10 scale; DotSelector uses 0–100. Map between them.
  export let sfxVolume = 5;
  export let musicVolume = 5;
  export let voiceVolume = 5;
  export let musicSource = 'game';
  export let radioEnabled = false;
  export let radioAutostart = false;
  export let radioChannel = 'all';
  export let radioQuality = 'medium';
  export let radioVolume = 70;
  export let scheduleSave;

  let dotSfx = Math.round(Number(sfxVolume || 0) * 10);
  let dotMusic = Math.round(Number(musicVolume || 0) * 10);
  let dotVoice = Math.round(Number(voiceVolume || 0) * 10);
  let dotRadio = Math.max(0, Math.min(100, Math.round(Number(radioVolume || 70))));
  let channelOptions = ['all'];

  function normalizeSource(value) {
    return value === 'midoriai_radio' ? 'midoriai_radio' : 'game';
  }

  function clampRadioVolume(value) {
    const numeric = Number(value);
    if (!Number.isFinite(numeric)) return 70;
    return Math.max(0, Math.min(100, Math.round(numeric)));
  }

  async function refreshChannels() {
    try {
      const payload = await getRadioChannels();
      const list = Array.isArray(payload?.data?.channels) ? payload.data.channels : [];
      const names = list
        .map((entry) => normalizeRadioChannel(entry?.name))
        .filter((name) => name !== 'all')
        .filter((name, index, arr) => arr.indexOf(name) === index)
        .sort((a, b) => a.localeCompare(b));
      channelOptions = ['all', ...names];
      if (!channelOptions.includes(radioChannel)) {
        radioChannel = 'all';
      }
    } catch {
      channelOptions = ['all'];
      if (radioChannel !== 'all') {
        radioChannel = 'all';
      }
    }
  }

  onMount(() => {
    void refreshChannels();
  });

  $: { const v = Math.round(Number(sfxVolume || 0) * 10); if (v !== dotSfx) dotSfx = v; }
  $: { const v = Math.round(Number(musicVolume || 0) * 10); if (v !== dotMusic) dotMusic = v; }
  $: { const v = Math.round(Number(voiceVolume || 0) * 10); if (v !== dotVoice) dotVoice = v; }
  $: {
    const v = clampRadioVolume(radioVolume);
    if (v !== dotRadio) dotRadio = v;
  }
  $: {
    const nextSource = normalizeSource(musicSource);
    if (nextSource !== musicSource) {
      musicSource = nextSource;
    }
  }
  $: {
    const normalized = normalizeRadioChannel(radioChannel);
    if (normalized !== radioChannel) {
      radioChannel = normalized;
    }
  }
  $: {
    const normalized = normalizeRadioQuality(radioQuality);
    if (normalized !== radioQuality) {
      radioQuality = normalized;
    }
  }
</script>

<div class="settings-panel">
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
      <DotSelector bind:value={dotMusic} on:change={() => { musicVolume = Math.round(dotMusic / 10); scheduleSave(); }} />
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
  <div class="control" title="Enable Midori AI Radio as a playable source.">
    <div class="control-left">
      <span class="label"><Power /> Enable Radio</span>
    </div>
    <div class="control-right">
      <label class="toggle">
        <input
          type="checkbox"
          bind:checked={radioEnabled}
          on:change={() => {
            radioEnabled = Boolean(radioEnabled);
            scheduleSave();
          }}
        />
        <span>On</span>
      </label>
    </div>
  </div>
  <div class="control" title="Automatically start radio playback when radio source is active.">
    <div class="control-left">
      <span class="label"><Music /> Radio Autostart</span>
    </div>
    <div class="control-right">
      <label class="toggle">
        <input
          type="checkbox"
          bind:checked={radioAutostart}
          on:change={() => {
            radioAutostart = Boolean(radioAutostart);
            scheduleSave();
          }}
        />
        <span>Auto</span>
      </label>
    </div>
  </div>
  <div class="control" title="Set preferred radio channel.">
    <div class="control-left">
      <span class="label"><Signal /> Radio Channel</span>
    </div>
    <div class="control-right">
      <label class="select-wrap">
        <span class="sr-only">Radio channel</span>
        <select
          bind:value={radioChannel}
          on:change={() => {
            radioChannel = normalizeRadioChannel(radioChannel);
            scheduleSave();
          }}
        >
          {#each channelOptions as channel}
            <option value={channel}>{channel}</option>
          {/each}
        </select>
      </label>
    </div>
  </div>
  <div class="control" title="Choose radio stream quality.">
    <div class="control-left">
      <span class="label"><Signal /> Radio Quality</span>
    </div>
    <div class="control-right">
      <label class="select-wrap">
        <span class="sr-only">Radio quality</span>
        <select
          bind:value={radioQuality}
          on:change={() => {
            radioQuality = normalizeRadioQuality(radioQuality);
            scheduleSave();
          }}
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </label>
    </div>
  </div>
  <div class="control" title="Adjust radio playback volume.">
    <div class="control-left">
      <span class="label"><Volume2 /> Radio Volume</span>
    </div>
    <div class="control-right">
      <DotSelector
        bind:value={dotRadio}
        on:change={() => {
          radioVolume = clampRadioVolume(dotRadio);
          scheduleSave();
        }}
      />
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

  .toggle {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    min-height: 1.9rem;
    user-select: none;
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
