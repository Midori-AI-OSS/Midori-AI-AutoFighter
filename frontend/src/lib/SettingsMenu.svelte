<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
  export let soundVol = 50;
  export let musicVol = 50;
  export let voiceVol = 50;

  function confirm() {
    dispatch('close');
  }
  function cancel() {
    dispatch('close');
  }
</script>

<style>
  .menu {
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
    background: rgba(0,0,0,0.65);
    border: 2px solid #777;
    padding: 1rem;
    box-sizing: border-box;
    backdrop-filter: blur(4px);
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  .actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
  }
  button {
    border: 2px solid #fff;
    background: #0a0a0a;
    color: #fff;
    padding: 0.3rem 0.6rem;
  }
</style>

<div class="menu">
  <h3>Settings</h3>
  <div>
    <label for="sound-vol">Sound Volume: {soundVol}%</label>
    <input id="sound-vol" type="range" min="0" max="100" bind:value={soundVol} />
  </div>
  <div>
    <label for="music-vol">Music Volume: {musicVol}%</label>
    <input id="music-vol" type="range" min="0" max="100" bind:value={musicVol} />
  </div>
  <div>
    <label for="voice-vol">Voice Volume: {voiceVol}%</label>
    <input id="voice-vol" type="range" min="0" max="100" bind:value={voiceVol} />
  </div>
  <div class="actions">
    <button on:click={cancel}>Cancel</button>
    <button on:click={confirm}>Confirm</button>
  </div>
</div>
