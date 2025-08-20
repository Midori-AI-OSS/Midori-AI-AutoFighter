# Continuous Integration Workflow

A GitHub Actions workflow runs tests and linting on each push and pull request.

The workflow is defined in `.github/workflows/ci.yml` and is split into individual parallel jobs for maximum granularity and performance:

## Backend Test Jobs (27 jobs)
Each backend test file runs in its own separate job using [`astral-sh/setup-uv`](https://github.com/astral-sh/setup-uv) with Python 3.12:
- `backend-test-aftertaste` - tests/test_aftertaste.py
- `backend-test-app` - tests/test_app.py  
- `backend-test-battle-timing` - tests/test_battle_timing.py
- `backend-test-card-rewards` - tests/test_card_rewards.py
- `backend-test-critical-boost` - tests/test_critical_boost.py
- `backend-test-damage-type-persistence` - tests/test_damage_type_persistence.py
- `backend-test-effects` - tests/test_effects.py
- `backend-test-enrage-stacking` - tests/test_enrage_stacking.py
- `backend-test-event-bus` - tests/test_event_bus.py
- `backend-test-exp-leveling` - tests/test_exp_leveling.py
- `backend-test-gacha` - tests/test_gacha.py
- `backend-test-loot-summary` - tests/test_loot_summary.py
- `backend-test-mapgen` - tests/test_mapgen.py
- `backend-test-party-endpoint` - tests/test_party_endpoint.py
- `backend-test-party-persistence` - tests/test_party_persistence.py
- `backend-test-passives` - tests/test_passives.py
- `backend-test-player-editor` - tests/test_player_editor.py
- `backend-test-player-plugins` - tests/test_player_plugins.py
- `backend-test-player-stats` - tests/test_player_stats.py
- `backend-test-player-stats-persistence` - tests/test_player_stats_persistence.py
- `backend-test-relic-rewards` - tests/test_relic_rewards.py
- `backend-test-relics` - tests/test_relics.py
- `backend-test-room-action` - tests/test_room_action.py
- `backend-test-save-management` - tests/test_save_management.py
- `backend-test-save-manager` - tests/test_save_manager.py
- `backend-test-shop-room` - tests/test_shop_room.py
- `backend-test-vitality-effects` - tests/test_vitality_effects.py

## Frontend Test Jobs (22 jobs) 
Each frontend test file runs in its own separate job using [`oven-sh/setup-bun`](https://github.com/oven-sh/setup-bun):
- `frontend-test-api` - api.test.js
- `frontend-test-assetloader` - assetloader.test.js
- `frontend-test-assets` - assets.test.js
- `frontend-test-battleview` - battleview.test.js
- `frontend-test-craftingmenu` - craftingmenu.test.js
- `frontend-test-feedback` - feedback.test.js
- `frontend-test-framerate-persistence` - frameratePersistence.test.js
- `frontend-test-gameviewport` - gameviewport.test.js
- `frontend-test-inventorypanel` - inventorypanel.test.js
- `frontend-test-layout` - layout.test.js
- `frontend-test-nonbattle` - nonbattle.test.js
- `frontend-test-partypersistence` - partypersistence.test.js
- `frontend-test-partypicker` - partypicker.test.js
- `frontend-test-playereditor` - playereditor.test.js
- `frontend-test-pullsmenu` - pullsmenu.test.js
- `frontend-test-restroom` - restroom.test.js
- `frontend-test-rewardloader` - rewardloader.test.js
- `frontend-test-rewardoverlay` - rewardoverlay.test.js
- `frontend-test-runpersistence` - runpersistence.test.js
- `frontend-test-settings-storage` - settingsStorage.test.js
- `frontend-test-settingsmenu` - settingsmenu.test.js
- `frontend-test-shopmenu` - shopmenu.test.js

## Linting Jobs (2 jobs)
- **backend-lint**: Uses `uv` to run `uvx ruff check backend` for Python code linting
- **frontend-lint**: Uses `bun` to run `eslint` for JavaScript code linting

This highly parallel structure (51 total jobs) provides maximum granularity for identifying specific test failures while allowing all tests to run simultaneously for fastest possible feedback.
