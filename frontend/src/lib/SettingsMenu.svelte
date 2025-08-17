<script>
  import { createEventDispatcher } from 'svelte';
  import { Volume2, Music, Mic, Power, Trash2, Download, Upload } from 'lucide-svelte';
  import { endRun, wipeData, exportSave, importSave } from './api.js';
  import { clearSettings } from './settingsStorage.js';

  const dispatch = createEventDispatcher();
  export let sfxVolume = 50;
  export let musicVolume = 50;
  export let voiceVolume = 50;
  export let framerate = 60;
  export let autocraft = false;
  export let runId = '';

  function save() {
    dispatch('save', {
      sfxVolume,
      musicVolume,
      voiceVolume,
      framerate: Number(framerate),
      autocraft
    });
  }


  async function handleEndRun() {
    if (runId) {
      await endRun(runId);
    }
  }

  async function handleWipe() {
    if (!confirm('This will erase all save data. Continue?')) return;
    await wipeData();
    clearSettings();
    sfxVolume = 50;
    musicVolume = 50;
    voiceVolume = 50;
    framerate = 60;
    autocraft = false;
    runId = '';
    alert('Save data wiped.');
  }

  async function handleBackup() {
    const blob = await exportSave();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'backup.afsave';
    a.click();
    URL.revokeObjectURL(url);
  }

  async function handleImport(event) {
    const [file] = event.target.files;
    if (file) {
      await importSave(file);
    }
  }
</script>

<div data-testid="settings-menu">
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
          <option value={30}>30</option>
          <option value={60}>60</option>
          <option value={120}>120</option>
        </select>
      </div>
      <div class="control" title="Clear all save data.">
        <Trash2 />
        <label>Wipe Save Data</label>
        <button on:click={handleWipe}>Wipe</button>
      </div>
      <div class="control" title="Download encrypted backup of save data.">
        <Download />
        <label>Backup Save Data</label>
        <button on:click={handleBackup}>Backup</button>
      </div>
      <div class="control" title="Import an encrypted save backup.">
        <Upload />
        <label>Import Save Data</label>
        <input type="file" accept=".afsave" on:change={handleImport} />
      </div>
    </div>
    <div class="col">
      <h4>Gameplay</h4>
      <div class="control" title="Automatically craft materials when possible.">
        <label>Autocraft</label>
        <input type="checkbox" bind:checked={autocraft} />
      </div>
      <div class="control" title="End the current run.">
        <Power />
        <label>End Run</label>
        <button on:click={handleEndRun} disabled={!runId}>End</button>
      </div>
    </div>
  </div>
  <div class="actions">
    <button on:click={save}>Save</button>
  </div>
</div>

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

