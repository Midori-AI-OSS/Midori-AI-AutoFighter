<script>
	import { createEventDispatcher } from 'svelte';
	import MenuPanel from './MenuPanel.svelte';
	const dispatch = createEventDispatcher();
        export let stats = { hp: 1000, def: 50, vitality: 1, regain: 1, exp: 1 };
	function close() { dispatch('close'); }
</script>

<MenuPanel data-testid="stats-panel" padding="0.75rem">
	<div class="stats-root">
		<header class="head">
			<h3>Stats</h3>
			<button class="mini" title="Close" on:click={close}>✕</button>
		</header>
		<div class="stats-grid">
			<div><span>HP</span><span>{stats.hp}</span></div>
			<div><span>DEF</span><span>{stats.def}</span></div>
			<div><span>Vitality</span><span>{stats.vitality}</span></div>
			<div><span>Regain</span><span>{stats.regain}</span></div>
			<div><span>EXP</span><span>{stats.exp}</span></div>
		</div>
	</div>
</MenuPanel>

<style>
	.stats-root { display:flex; flex-direction:column; gap:0.8rem; }
	.head { display:flex; align-items:center; }
	.head h3 { margin:0; font-size:1rem; }
	.head .mini { margin-left:auto; }
	.mini { border:1px solid #fff; background:#111; color:#fff; font-size:0.7rem; padding:0.25rem 0.45rem; cursor:pointer; }
	.stats-grid { display:grid; grid-template-columns: repeat(auto-fill,minmax(120px,1fr)); gap:0.4rem 0.8rem; }
	.stats-grid > div { display:flex; justify-content:space-between; background:rgba(255,255,255,0.05); padding:0.35rem 0.55rem; font-size:0.75rem; border:1px solid rgba(255,255,255,0.08); }
</style>
