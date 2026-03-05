<script>
  import { Music, Power } from 'lucide-svelte';

  export let radioEnabled = false;
  export let radioAutostart = false;
  export let scheduleSave;
</script>

<div class="settings-panel">
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

  <div class="control" title="Automatically start playback when Midori AI Radio source is active.">
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
</div>

<style>
  @import './settings-shared.css';

  .toggle {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    min-height: 1.9rem;
    user-select: none;
  }
</style>
