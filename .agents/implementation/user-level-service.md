# User Level Service

Tracks persistent user experience and level progression.

## Functions
- `get_user_state()` – return current level, experience, and next level threshold.
- `get_user_level()` – convenience wrapper returning only the level.
- `gain_user_exp(amount)` – add experience and handle level ups.
- `apply_user_level_to_party(party)` – reapply level-based stat hooks to every party member.

Use `apply_user_level_to_party` after user experience changes so party stats reflect the latest level.
