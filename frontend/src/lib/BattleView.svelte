<script>
  import MenuPanel from './MenuPanel.svelte';
  import { getCharacterImage, getRandomBackground, getElementColor } from './assetLoader.js';
  export let party = [];
  let bg = getRandomBackground();
</script>

<div class="battle-field" style={`background-image: url(${bg})`} data-testid="battle-view">
  <MenuPanel>
    <h3>Battle</h3>
    {#if party.length}
      <div class="party-line">
        {#each party as member}
          <img src={getCharacterImage(member.id)} alt="" class="party-icon" style={`border-color: ${getElementColor(member.element)}`} />
        {/each}
      </div>
    {/if}
    <p>Combat UI placeholder.</p>
  </MenuPanel>
</div>

<style>
  .battle-field {
    position: absolute;
    inset: 0;
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  p {
    margin: 0.5rem 0 0 0;
  }
  .party-line {
    display: flex;
    gap: 0.25rem;
    margin-bottom: 0.5rem;
  }
  .party-icon {
    width: 32px;
    height: 32px;
    border: 2px solid #555;
    border-radius: 4px;
  }
</style>
