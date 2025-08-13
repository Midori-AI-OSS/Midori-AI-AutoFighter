# Lock player stat editing during runs
Ensure the backend blocks stat allocation changes once a run has begun. Parent: [UI Foundation](../planning/e26e5ed7-ui-foundation-plan.md).

## Requirements
- Prevent character editor endpoints from applying stat changes while a run is active.
- Allow edits again after the run ends.
- Return a clear error when an edit is attempted mid-run.

## Acceptance Criteria
- Editing stats during an active run returns an error.
- Tests cover allowed edits before runs, blocked edits mid-run, and edits after a run completes.
