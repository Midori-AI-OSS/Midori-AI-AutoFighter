<script>
  import MenuPanel from './MenuPanel.svelte';
  import { createEventDispatcher } from 'svelte';
  export let pronouns = '';
  export let damageType = 'Light';
  export let hp = 0;
  export let attack = 0;
  export let defense = 0;
  const maxPoints = 100;
  const dispatch = createEventDispatcher();

  $: remaining = maxPoints - hp - attack - defense;

  function close() { dispatch('close'); }
  function save() {
    dispatch('save', {
      pronouns,
      damageType,
      hp: +hp,
      attack: +attack,
      defense: +defense,
    });
  }
</script>

<MenuPanel data-testid="player-editor" padding="0.75rem">
  <div class="editor">
    <header class="editor-header">
      <h3>Player Editor</h3>
      <div class="spacer" />
      <button class="mini" on:click={close} title="Close">✕</button>
    </header>
    <div class="grid">
      <label for="pronouns">Pronouns</label>
      <input id="pronouns" type="text" maxlength="15" bind:value={pronouns} />
      <label for="damage">Damage Type</label>
      <select id="damage" bind:value={damageType}>
        <option>Light</option>
        <option>Dark</option>
        <option>Wind</option>
        <option>Lightning</option>
        <option>Fire</option>
        <option>Ice</option>
      </select>
    </div>
    <div class="stats">
      <p class="remaining">Points remaining: {remaining}</p>
      <div class="stat-row">
        <label for="hp">HP: {hp}</label>
        <input id="hp" type="range" min="0" max={hp + remaining} bind:value={hp} />
      </div>
      <div class="stat-row">
        <label for="attack">Attack: {attack}</label>
        <input id="attack" type="range" min="0" max={attack + remaining} bind:value={attack} />
      </div>
      <div class="stat-row">
        <label for="defense">Defense: {defense}</label>
        <input id="defense" type="range" min="0" max={defense + remaining} bind:value={defense} />
      </div>
    </div>
    <div class="actions">
      <button class="primary" on:click={save}>Save</button>
      <button on:click={close}>Close</button>
    </div>
  </div>
</MenuPanel>

<style>
  .editor { display:flex; flex-direction:column; gap:0.9rem; }
  .editor-header { display:flex; align-items:center; gap:0.5rem; }
  .editor-header h3 { margin:0; font-size:1rem; }
  .spacer { flex:1; }
  .grid { display:grid; grid-template-columns: 120px 1fr; gap:0.4rem 0.6rem; align-items:center; }
  .stats { display:flex; flex-direction:column; gap:0.4rem; }
  .stat-row { display:flex; flex-direction:column; gap:0.2rem; }
  .remaining { margin:0 0 0.2rem 0; font-size:0.85rem; opacity:0.85; }
  .actions { display:flex; justify-content:flex-end; gap:0.5rem; }
  button { border:1px solid #fff; background:#0a0a0a; color:#fff; padding:0.35rem 0.8rem; cursor:pointer; font-size:0.8rem; }
  button.primary { background:rgba(120,180,255,0.18); }
  button.primary:hover { background:rgba(120,180,255,0.32); }
  button.mini { padding:0.2rem 0.45rem; font-size:0.7rem; }
  input[type="text"], select { background:#111; border:1px solid #555; color:#fff; padding:0.25rem 0.4rem; font-size:0.8rem; }
  input[type="range"] { width:100%; }
</style>
