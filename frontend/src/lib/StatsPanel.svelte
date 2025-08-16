<script>
        export let stats = { hp: 1000, def: 50, vitality: 1, regain: 1, exp: 1 };
</script>

<div class="stats-root" data-testid="stats-panel">
        <div class="stats-grid">
                <div><span>HP</span><span>{stats.hp}</span></div>
                <div><span>DEF</span><span>{stats.def}</span></div>
                <div><span>Vitality</span><span>{stats.vitality}</span></div>
                <div><span>Regain</span><span>{stats.regain}</span></div>
                <div><span>EXP</span><span>{stats.exp}</span></div>
        </div>
</div>

<style>
        .stats-root { display:flex; flex-direction:column; gap:0.8rem; }
        .stats-grid { display:grid; grid-template-columns: repeat(auto-fill,minmax(120px,1fr)); gap:0.4rem 0.8rem; }
        .stats-grid > div { display:flex; justify-content:space-between; background:rgba(255,255,255,0.05); padding:0.35rem 0.55rem; font-size:0.75rem; border:1px solid rgba(255,255,255,0.08); }
</style>
