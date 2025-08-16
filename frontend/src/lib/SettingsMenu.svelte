<script>
  import MenuPanel from './MenuPanel.svelte';
  import { createEventDispatcher } from 'svelte';
  import { Volume2, Music, Mic } from 'lucide-svelte';

  const dispatch = createEventDispatcher();
  export let sfxVolume = 50;
  export let musicVolume = 50;
  export let voiceVolume = 50;
  export let framerate = 60;
  export let autocraft = false;

  function save() {
    dispatch('save', {
      sfxVolume,
      musicVolume,
      voiceVolume,
      framerate: Number(framerate),
      autocraft
    });
  }

  function close() {
    dispatch('close');
  }
</script>

<MenuPanel data-testid="settings-menu">
  <h3>Settings</h3>
  <div class="cols">
    <div class="col">
      <h4>Audio</h4>
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
      <div class="control" title="Adjust voice volume.">
        <Mic />
        <label>Voice Volume</label>
        <input type="range" min="0" max="100" bind:value={voiceVolume} />
      </div>
    </div>
    <div class="col">
      <h4>System</h4>
      <div class="control" title="Limit server polling frequency.">
        <label>Framerate</label>
        <select bind:value={framerate}>
          <option value="30">30</option>
          <option value="60">60</option>
          <option value="120">120</option>
        </select>
      </div>
    </div>
    <div class="col">
      <h4>Gameplay</h4>
      <div class="control" title="Automatically craft materials when possible.">
        <label>Autocraft</label>
        <input type="checkbox" bind:checked={autocraft} />
      </div>
    </div>
  </div>
  <div class="actions">
    <button on:click={save}>Save</button>
    <button on:click={close}>Close</button>
  </div>
</MenuPanel>

<style>
  .cols {
    display: flex;
    gap: 1rem;
  }

  .col {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  h4 {
    margin: 0 0 0.25rem 0;
    font-size: 1rem;
  }

  .control {
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }

  label {
    flex: 1;
    font-size: 0.85rem;
  }

  input[type='range'] {
    flex: 2;
  }

  select {
    flex: 2;
    background: #0a0a0a;
    color: #fff;
    border: 1px solid #fff;
  }

  .actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    margin-top: 0.5rem;
  }

  button {
    border: 2px solid #fff;
    background: #0a0a0a;
    color: #fff;
    padding: 0.3rem 0.6rem;
  }
</style>

