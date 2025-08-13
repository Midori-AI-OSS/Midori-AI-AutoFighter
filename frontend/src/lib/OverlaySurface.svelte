<script>
  export let padding = '0.4rem 0.75rem 0.75rem 0.75rem';
</script>

<style>
  .surface {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: var(--ui-top-offset);
    display: flex;
    padding: var(--padding);
    box-sizing: border-box;
    z-index: 5;
    overflow: hidden;
  }
</style>

<div class="surface" style={`--padding: ${padding}`}>
  <slot />
</div>
