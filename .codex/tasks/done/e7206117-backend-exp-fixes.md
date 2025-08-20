# Backend XP and Party Persistence Fixes

## Summary
Investigate and address leveling and healing anomalies while updating docs to reflect experience mechanics.

## Tasks
1. **Buff low-level experience and verify leveling**  
   - File: `backend/autofighter/stats.py` lines 75-82.  
   - Adjust `gain_exp` so characters below level 1000 receive a boosted experience multiplier and level up correctly.  
   - Add a unit test confirming that granting sufficient XP increases `Stats.level` and carries over to the run party.

2. **Persist party state across fights without unintended healing**  
   - File: `backend/autofighter/rooms.py` lines 192-210 and 360-365.  
   - Review deep-copy logic and synchronization back to `party` to ensure HP and other stats persist between battles.  
   - Remove or correct any code that resets HP when starting a new fight and add a regression test covering HP persistence.

3. **Audit passives that heal on room entry**  
   - File: `backend/plugins/passives/room_heal.py` lines 5-13.  
   - Determine whether `RoomHeal` or similar passives are unintentionally attached to party members, causing heals between encounters.  
   - Adjust battle initialization or passive assignment so healing only occurs when explicitly triggered.

4. **Update documentation for experience mechanics**  
   - File: `README.md` line 137.  
     - Add a paragraph under **Battle Room** explaining experience rewards, level-ups, and the sub-1000 level XP buff.  
   - File: `backend/README.md` line 16.  
     - Document how battle resolution awards XP and levels to all party members.  
   - File: `.codex/implementation/stats-and-effects.md` line 5.  
     - Expand the Stats field overview with details on level-up behavior and the low-level XP multiplier.  
   - File: `.codex/implementation/battle-room.md` line 11.
     - Clarify that `BattleRoom` deep-copies the party for combat and syncs final stats (including XP) back to the run.

Status: Need Review
