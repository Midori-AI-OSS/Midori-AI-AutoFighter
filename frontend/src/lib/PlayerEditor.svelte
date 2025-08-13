<script>
  import MenuPanel from './MenuPanel.svelte';
  import { createEventDispatcher, onMount } from 'svelte';
  export let pronouns = '';
  export let damage = 'Light';
  export let hp = 0;
  export let attack = 0;
  export let defense = 0;
  const maxPoints = 100;
  const dispatch = createEventDispatcher();
  let ready = false;
  onMount(() => { ready = true; });
  $: remaining = maxPoints - hp - attack - defense;
  $: if (ready) {
    dispatch('save', { pronouns, damage, hp, attack, defense });
  }
  function close() { dispatch('close'); }
</script>

<MenuPanel data-testid="player-editor">
  <div class="editor">
    <h3>Player Editor</h3>
    <div>
      <label for="pronouns">Pronouns</label>
      <input id="pronouns" type="text" maxlength="15" bind:value={pronouns} />
    </div>
    <div>
      <label for="damage">Damage Type</label>
      <select id="damage" bind:value={damage}>
        <option>Light</option>
        <option>Dark</option>
        <option>Wind</option>
        <option>Lightning</option>
        <option>Fire</option>
        <option>Ice</option>
      </select>
    </div>
    <div class="stats">
      <p>Points remaining: {remaining}</p>
      <label for="hp">HP: {hp}</label>
      <input id="hp" type="range" min="0" max={hp + remaining} bind:value={hp} />
      <label for="attack">Attack: {attack}</label>
      <input id="attack" type="range" min="0" max={attack + remaining} bind:value={attack} />
      <label for="defense">Defense: {defense}</label>
      <input id="defense" type="range" min="0" max={defense + remaining} bind:value={defense} />
    </div>
    <div class="actions">
      <button on:click={close}>Close</button>
    </div>
  </div>
</MenuPanel>

<style>
  .editor {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  .stats {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
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
