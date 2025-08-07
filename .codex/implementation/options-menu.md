# Options Menu

The Options submenu provides in-game controls for audio levels and stat screen behaviour.
Implemented in `game/ui/options.py` and invoked from the Main Menu.

## Audio Controls
- **SFX Volume** – DirectGUI slider linked to `AudioManager.set_sfx_volume` and stored in settings.
- **Music Volume** – Slider that updates `AudioManager.set_music_volume` for background tracks.

## Stat Screen Settings
- **Refresh Rate** – Slider selecting 1–10 frame intervals; saves to `app.stat_refresh_rate` and settings.
- **Pause on Stat Screen** – Toggle that suspends gameplay tasks while stats are open.

## Persistence and Navigation
- All options save immediately via `save_settings` so values persist across sessions.
- Arrow keys adjust sliders, and Enter activates the highlighted widget.
