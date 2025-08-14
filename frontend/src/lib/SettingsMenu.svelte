<script>
  import MenuPanel from './MenuPanel.svelte';
  import { createEventDispatcher } from 'svelte';
  import { Volume2, Music, Pause } from 'lucide-svelte';

  const dispatch = createEventDispatcher();
  export let sfxVolume = 50;
  export let musicVolume = 50;
  export let pauseOnStats = false;

  function close() {
    dispatch('close');
  }
</script>

<MenuPanel data-testid="settings-menu">
  <h3>Settings</h3>
  <div class="control" title="Adjust sound effect volume.">
    <Volume2 />
    <label>SFX Volume</label>
    <input type="range" min="0" max="100" bind:value={sfxVolume} />
  </div>
  <div class="control" title="Adjust background music volume.">
    <Music />
    <label>Music Volume</label>
    <input type="range" min="0" max="100" bind:value={musicVolume} />
  </div>
  <div class="control" title="Stop gameplay while viewing stats.">
    <Pause />
    <label>Pause on Stat Screen</label>
    <input type="checkbox" bind:checked={pauseOnStats} />
  </div>
  <div class="actions">
    <button on:click={close}>Close</button>
  </div>
</MenuPanel>

<style>
  .control {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin-bottom: 0.5rem;
  }
  label {
    flex: 1;
    font-size: 0.85rem;
  }
  input[type='range'] {
    flex: 2;
  }
  .actions {
    display: flex;
    justify-content: flex-end;
  }
  button {
    border: 2px solid #fff;
    background: #0a0a0a;
    color: #fff;
    padding: 0.3rem 0.6rem;
  }
</style>
