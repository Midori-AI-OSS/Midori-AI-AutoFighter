# Action Value Display

Developers can overlay numeric action values in the turn order UI to debug queue calculations.

## Enabling

- Set environment variable `SHOW_ACTION_VALUES=1` before starting the backend, or
- Launch the server with `--show-action-values` if using the CLI.

The frontend reads the `show_action_values` flag from battle snapshots and will display numbers alongside portraits when enabled.

## Disabling

Unset the environment variable or omit the flag to hide action values. Players can also toggle the display in **Options → Gameplay → Show Action Values**.

## Related Docs

- [Action Queue and Timing](../implementation/battle-room.md)
- [Action Queue Docs task](../tasks/e83ce5e6-action-queue-docs.md)
