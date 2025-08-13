<script>
  export let padding = '0.5rem';
</script>

<style>
  .panel {
    width: 99%;
    height: 99%;
    max-width: 99%;
    max-height: 99%;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    padding: var(--padding);
    overflow: auto;
    border: 2px solid #777;
    background: rgba(0,0,0,0.65);
    backdrop-filter: blur(4px);
  }
</style>

<div class="panel" style={`--padding: ${padding}`}> 
  <slot />
</div>
