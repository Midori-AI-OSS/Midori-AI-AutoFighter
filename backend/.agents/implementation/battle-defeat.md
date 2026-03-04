# Battle defeat handling

`BattleRoom.resolve` reports a `"defeat"` result when all party members have zero or less HP and includes `ended: true` in the snapshot. `_run_battle` checks for this outcome, clears pending state flags, saves the final snapshot, and removes the run from storage.
