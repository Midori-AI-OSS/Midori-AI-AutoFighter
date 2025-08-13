<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import MenuPanel from './MenuPanel.svelte';
  const dispatch = createEventDispatcher();
  export let soundVol = 50;
  export let musicVol = 50;
  export let voiceVol = 50;
  export let frameCap = 30;
  export let theme = 'dark';
  $: pollRate = Math.round(1000 / frameCap);
  let ready = false;
  onMount(() => {
    ready = true;
  });
  $: if (ready) {
    dispatch('save', { soundVol, musicVol, voiceVol, frameCap, pollRate, theme });
  }
  function close() {
    dispatch('close');
  }
</script>

<style>
  .menu {
    flex: 1;
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

<MenuPanel>
  <div class="menu">
    <h3>Settings</h3>
    <section>
      <h4>Audio</h4>
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
    </section>
    <section>
      <h4>Gameplay</h4>
      <div>
        <label for="theme">Theme:</label>
        <select id="theme" bind:value={theme}>
          <option value="light">Light</option>
          <option value="dark">Dark</option>
          <option value="editable">Editable</option>
        </select>
      </div>
    </section>
    <section>
      <h4>Server</h4>
      <div>
        <label for="frame-cap">Frame Rate Cap:</label>
        <select id="frame-cap" bind:value={frameCap}>
          <option value={30}>30</option>
          <option value={60}>60</option>
          <option value={120}>120</option>
        </select>
        <span>Polling Rate: {pollRate} ms</span>
      </div>
    </section>
    <div class="actions">
      <button on:click={close}>Close</button>
    </div>
  </div>
</MenuPanel>
