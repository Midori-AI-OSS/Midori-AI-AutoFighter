<script>
  import { onMount } from 'svelte';
  import { getPlayers } from './api.js';
  import { Flame, Snowflake, Zap, Sun, Moon, Wind, Circle } from 'lucide-svelte';
  import { getCharacterImage, getHourlyBackground, getRandomFallback } from './assetLoader.js';
  import MenuPanel from './MenuPanel.svelte';

  let background = '';

  let roster = [];
  let error = '';

  export let selected = [];
  export let compact = false;
  let previewId;

  let activeTab = 'Core';
  const statTabs = ['Core', 'Offense', 'Defense'];

  onMount(async () => {
    background = getHourlyBackground();
    try {
      const data = await getPlayers();
      roster = data.players
        .map(p => ({
          id: p.id,
          name: p.name,
          img: getCharacterImage(p.id, p.is_player) || getRandomFallback(),
          owned: p.owned,
          is_player: p.is_player,
          element: p.element ?? 'Generic',
          stats: p.stats ?? { hp: 0, atk: 0, defense: 0, level: 1 }
        }))
        .filter(p => p.owned || p.is_player)
        .sort((a, b) => (a.is_player ? -1 : b.is_player ? 1 : 0));
      const player = roster.find(p => p.is_player);
      if (player) {
        selected = [player.id];
        previewId = player.id;
      }
    } catch (e) {
      error = 'Unable to load roster. Is the backend running on 59002?';
    }
  });

  function select(id) {
    const char = roster.find(c => c.id === id);
    if (char) {
      previewId = id;
    }
  }

  function toggleMember() {
    if (!previewId) return;
    if (selected.includes(previewId)) {
      selected = selected.filter(c => c !== previewId);
    } else if (selected.length < 4) {
      selected = [...selected, previewId];
    }
  }

  function iconFor(element) {
    const e = (element || '').toLowerCase();
    if (e === 'fire') return Flame;
    if (e === 'ice') return Snowflake;
    if (e === 'lightning') return Zap;
    if (e === 'light') return Sun;
    if (e === 'dark') return Moon;
    if (e === 'wind') return Wind;
    return Circle;
  }
</script>

<style>
  .panel {
    border: 2px solid #fff;
    padding: 1rem;
    background: #000;
    background-size: cover;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: min(90vw, 480px);
    max-height: 80vh;
  }
  .full {
  display: grid;
  grid-template-columns: minmax(8rem, 22%) 1fr minmax(12rem, 26%);
  width: 100%;
  height: 96%;
  max-width: 100%;
  max-height: 98%;
  /* allow internal scrolling instead of clipping when content grows */
  
  }
  .panel.compact {
    width: 100%;
    max-width: none;
    background: #0a0a0a;
    background-image: none !important;
    border-color: #555;
    padding: 0.5rem;
    max-height: 200px;
  }
  .roster {
    overflow-y: auto;
    mask-image: linear-gradient(to bottom, transparent, black 5%, black 95%, transparent);
    -webkit-mask-image: linear-gradient(to bottom, transparent, black 5%, black 95%, transparent);
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 0.5rem 0;
    height: 98%;
    gap: 0.75rem;
    background: rgba(0,0,0,0.7);
    color: #fff;
    padding: 0.5rem 0.75rem;
    width: 100%;
    justify-content: flex-start;
    transition: all 0.2s ease;
    backdrop-filter: blur(2px);
  }
  .char-btn:hover {
    border-color: #888;
    background: rgba(20,20,20,0.8);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  }
  .panel.compact .char-btn {
    background: transparent;
    border: none;
    padding: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  .char-btn img {
    width: 40px;
    height: 40px;
    border-radius: 6px;
    border: 2px solid #333;
    object-fit: cover;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
  }
  .char-btn.selected img {
    border-color: #000;
    box-shadow: 0 2px 12px rgba(0,0,0,0.6);
  }
  .panel.compact .char-btn img { 
    width: 24px; 
    height: 24px;
    border-radius: 4px;
    border-width: 1px;
  }
  :global(.elem) { width: 18px; height: 18px; opacity: 0.85; }
  .preview {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    min-width: 0;
    min-height: 0;
  }
  .preview img {
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    border: 3px solid #555;
    background: #222;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    display: block;
    margin: 0 auto;
  }
  /* New stats panel styling */
  .stats-panel {
    flex: 1;
    width: 350px;
    background: rgba(0,0,0,0.25);
    border-left: 2px solid #444;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    box-sizing: border-box;
    border-radius: 8px;
  }
  .stats-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    border-bottom: 1px solid rgba(255,255,255,0.2);
    padding-bottom: 0.5rem;
  }
  .char-name {
    font-size: 1.2rem;
    color: #fff;
    flex: 1;
  }
  .char-level {
    font-size: 1rem;
    color: #ccc;
  }
  .type-icon {
    width: 24px;
    height: 24px;
  }
  /* Element type colors */
  .type-icon.fire { color: #e25822; }
  .type-icon.ice { color: #82caff; }
  .type-icon.lightning { color: #ffd700; }
  .type-icon.light { color: #ffff99; }
  .type-icon.dark { color: #8a2be2; }
  .type-icon.wind { color: #7fff7f; }
  .stats-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .stats-list div {
    display: flex;
    justify-content: space-between;
    color: #ddd;
  }
  .stats-placeholder {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #888;
    font-style: italic;
  }
  .stats-confirm {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  min-height: 32px;
  padding: 0.15rem 0;
  margin-top: 0.25rem;
  }
  button.confirm {
  border: 1.5px solid #fff;
  background: transparent;
  color: #fff;
  padding: 0.12rem 0.4rem;
  align-self: flex-end;
  font-size: 0.95rem;
  min-height: 28px;
  border-radius: 6px;
  }
  .roster-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(0, 25%));
    gap: 0.4rem;
    padding: 0.4rem;
    height: 100%;
    overflow-y: auto;
    justify-content: stretch;
    border-right: 2px solid #444;
    border-left: 2px solid #444;
    min-width: 0;
  }
  .char-card {
  position: relative;
  cursor: pointer;
  border: 2px solid transparent;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
  transition: all 0.2s ease;
  width: 100%;
  aspect-ratio: 1;
  max-height: 100%;
  margin: 0 auto;
  padding: 0;
  background: none;
  }
  .char-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  }
  .char-card.selected {
    border-color: #FFD700;
    box-shadow: 0 0 12px rgba(255,215,0,0.6);
  }
  .card-img {
  width: 100%;
  height: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  display: block;
  margin: 0 auto;
  }
  .card-overlay {
    position: absolute;
    bottom: 0;
    width: 100%;
    background: rgba(0,0,0,0.6);
    padding: 0.25rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
  }
  .card-name {
    color: #fff;
    font-size: 0.85rem;
    text-align: center;
  }
  .card-level {
    color: #ccc;
    font-size: 0.75rem;
  }
  .stats-tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }
  .tab-btn {
    background: rgba(255,255,255,0.1);
    color: #ddd;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.2s;
  }
  .tab-btn.active {
    background: rgba(255,255,255,0.3);
    color: #fff;
  }
  /* Party compact icons */
  .party-icon {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: #000;
    border: 2px solid currentColor; 
    color: currentColor; 
  }
  /* Compact mode: small photo thumbnails in side panel */
  .roster.list.compact {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem;
    background: transparent;
    border: none;
    min-height: 32px;
    height: auto;
  }
  .roster.list.compact .char-btn {
    border: none;
    background: transparent;
    padding: 0;
    flex-shrink: 0;
  }
  .roster.list.compact .char-btn img {
    width: 28px;
    height: 28px;
    border-radius: 4px;
    object-fit: cover;
    border: 1px solid #fff;
  }
</style>

  {#if compact}
  <!-- compact mode: small portrait thumbnails for party side menu -->
  <div class="roster list compact" data-testid="roster">
    {#each roster.filter(c => selected.includes(c.id)) as char}
      <button
        data-testid={`choice-${char.id}`}
        class="char-btn"
        on:click={() => select(char.id)}>
        <img src={char.img} alt={char.name} class="compact-img" />
      </button>
    {/each}
  </div>
{:else}
  <MenuPanel>
  <div class="full" data-testid="party-picker">
    <!-- Left: Roster grid cards -->
    <div class="roster-grid">
      {#each roster as char}
        <button type="button"
          data-testid={`choice-${char.id}`}
          class="char-card"
          class:selected={selected.includes(char.id)}
          on:click={() => select(char.id)}>
          <img src={char.img} alt={char.name} class="card-img" />
          <div class="card-overlay">
            <!-- use default small element icon -->
            <svelte:component this={iconFor(char.element)} class="elem" aria-hidden="true" />
            <span class="card-name">{char.name}</span>
            <span class="card-level">LVL {char.stats.level}</span>
          </div>
        </button>
      {/each}
    </div>

    <!-- Center: Portrait preview of selected -->
    <div class="preview">
      {#if previewId}
        {#each roster.filter(r => r.id === previewId) as sel}
          <img src={sel.img} alt={sel.name} />
        {/each}
      {:else}
        <div class="placeholder">Select up to 4 allies</div>
      {/if}
    </div>

    <!-- Right: Character Stats -->
    <div class="stats-panel" data-testid="stats-panel">
      <!-- Tab buttons for stats categories -->
      <div class="stats-tabs">
        {#each statTabs as tab}
          <button class="tab-btn" class:active={activeTab === tab} on:click={() => activeTab = tab}>
            {tab}
          </button>
        {/each}
      </div>
      {#if previewId}
        {#each roster.filter(r => r.id === previewId) as sel}
          <div class="stats-header">
            <span class="char-name">{sel.name}</span>
            <span class="char-level">Lv {sel.stats.level}</span>
            <svelte:component this={iconFor(sel.element)}
              class={`type-icon ${sel.element.toLowerCase()}`}
              aria-hidden="true" />
          </div>
          <div class="stats-list">
            {#if activeTab === 'Core'}
              <div><span>HP</span><span>{sel.stats.hp ?? '-'}</span></div>
              <div><span>DEF</span><span>{sel.stats.defense ?? '-'}</span></div>
              <div><span>Vitality</span><span>{sel.stats.vitality ?? sel.stats.vita ?? '-'}</span></div>
              <div><span>Regain</span><span>{sel.stats.regain ?? sel.stats.regain_rate ?? '-'}</span></div>
              <div><span>EXP</span><span>{sel.stats.exp ?? sel.stats.xp ?? '-'}</span></div>
            {:else if activeTab === 'Offense'}
              <div><span>ATK</span><span>{sel.stats.atk ?? '-'}</span></div>
              <div><span>CRIT Rate</span><span>{(sel.stats.critRate ?? sel.stats.crit_rate ?? 0) + '%'}</span></div>
              <div><span>CRIT DMG</span><span>{(sel.stats.critDamage ?? sel.stats.crit_dmg ?? 0) + '%'}</span></div>
              <div><span>Effect Hit Rate</span><span>{(sel.stats.effectHit ?? sel.stats.effect_hit ?? 0) + '%'}</span></div>
            {:else if activeTab === 'Defense'}
              <div><span>Mitigation</span><span>{sel.stats.mitigation ?? '-'}</span></div>
              <div><span>Dodge Odds</span><span>{sel.stats.dodge ?? sel.stats.dodgeOdds ?? '-'}</span></div>
              <div><span>Effect Resist</span><span>{sel.stats.effectResist ?? sel.stats.effect_res ?? '-'}</span></div>
            {/if}
          </div>
        {/each}
      {:else}
        <div class="stats-placeholder">Select a character to view stats</div>
      {/if}
      {#if previewId}
        <div class="stats-confirm">
          <button class="confirm" on:click={toggleMember}>
            {selected.includes(previewId) ? 'Remove from party' : 'Add to party'}
          </button>
        </div>
      {/if}
    </div>
  </div>
  </MenuPanel>
{/if}
