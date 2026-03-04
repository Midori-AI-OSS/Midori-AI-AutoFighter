# LRM Settings

The Settings menu surfaces language reasoning model selection.

- `settingsStorage.js` stores `lrmModel` alongside other options.
- `SettingsMenu.svelte` loads available models from `/config/lrm`, persists the selection locally and with `setLrmModel()`, and offers a **Test Model** button that posts a sample prompt via `testLrmModel()`.
- `api.js` exposes `getLrmConfig()`, `setLrmModel()`, and `testLrmModel()` helpers.

Reduced Motion is also surfaced here and disables non‑essential animations
(e.g., party selection sweep and ambient orbs). The **End Run** action now
immediately halts battle polling client‑side to ensure a clean return to the
main menu.
