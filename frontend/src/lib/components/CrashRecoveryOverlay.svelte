<!--
  CrashRecoveryOverlay.svelte
  
  Wrapper around ErrorOverlay for displaying persisted errors from previous session crashes.
  This component adds:
  - Header explaining this is from a previous session
  - Error acknowledgment API call on dismiss
  - Count of additional errors if multiple exist
  
  For displaying a single real-time error, use ErrorOverlay directly.
-->
<script>
  import { createEventDispatcher } from 'svelte';
  import ErrorOverlay from './ErrorOverlay.svelte';
  import { acknowledgePreviousErrors } from '../systems/api.js';

  export let errors = [];
  export let reducedMotion = false;

  const dispatch = createEventDispatcher();

  $: latestError = errors.length > 0 ? errors[errors.length - 1] : null;
  $: errorMessage = latestError ? `[Previous Session] ${latestError.message || 'Unknown error'}` : 'Unknown error from previous session';
  $: errorTraceback = latestError?.traceback || '';
  $: errorContext = latestError?.context ?? null;

  let acknowledgeFailed = false;

  async function handleClose() {
    acknowledgeFailed = false;
    try {
      await acknowledgePreviousErrors();
    } catch (e) {
      acknowledgeFailed = true;
      console.warn('Failed to acknowledge errors:', e);
      // Still close - errors will show again on next load
    }
    dispatch('close');
  }
</script>

<!-- Reuse the existing ErrorOverlay component for consistency -->
<ErrorOverlay
  message={errorMessage}
  traceback={errorTraceback}
  context={errorContext}
  {reducedMotion}
  on:close={handleClose}
/>
