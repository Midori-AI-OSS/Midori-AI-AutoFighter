import logging

from panda3d.core import WindowProperties
from direct.showbase.ShowBase import ShowBase

from plugins.event_bus import EventBus
from autofighter.audio import get_audio
from autofighter.save import load_settings
from autofighter.scene import SceneManager
from plugins.plugin_loader import PluginLoader
from autofighter.gui import BASE_WIDTH, BASE_HEIGHT


logger = logging.getLogger(__name__)


class AutoFighterApp(ShowBase):
    def __init__(self) -> None:
        super().__init__()

        logging.basicConfig(level=logging.INFO)
        logger.info("Panda3D initialized successfully")

        self.scene_manager = SceneManager(self)
        self.event_bus = EventBus()
        self.plugin_loader = PluginLoader(
            self.event_bus,
            required=[
                "player",
                "foe",
                "passive",
                "dot",
                "hot",
                "weapon",
                "room",
                "event",
            ],
        )
        self.plugin_loader.discover("plugins")
        self.plugin_loader.discover("mods")

        settings = load_settings()
        audio = get_audio()
        audio.set_sfx_volume(settings["sfx_volume"])
        audio.set_music_volume(settings["music_volume"])
        self.pause_on_stats = settings["pause_on_stats"]
        self.stat_refresh_rate = settings["stat_refresh_rate"]
        self.paused = False

        props = WindowProperties()
        props.set_title("Midori AI AutoFighter")
        props.set_size(BASE_WIDTH, BASE_HEIGHT)
        props.set_fixed_size(True)
        # Add window decorations control for OS compatibility
        props.set_minimized(False)
        props.set_undecorated(False)  # Ensure proper OS window controls
        self.win.request_properties(props)

        self.accept("window-event", self.on_window_event)
        self.accept("escape", self.userExit)

        self.setBackgroundColor(0, 0, 0, 1)

        # Removed placeholder model so only the main menu UI is visible

        self.task_mgr.add(self.update, "update")

        # Main menu will be reintroduced after the GUI overhaul

    def on_window_event(self, window) -> None:
        """Handle window events while maintaining 16:9 aspect ratio."""
        if window and window.is_closed():
            self.userExit()
            return

        # Enforce fixed size and aspect ratio to prevent horizontal stretching
        if window:
            current_props = window.get_properties()
            current_width = current_props.get_x_size()
            current_height = current_props.get_y_size()
            
            # Only reset if the size has actually changed from our target
            if current_width != BASE_WIDTH or current_height != BASE_HEIGHT:
                props = WindowProperties()
                props.set_size(BASE_WIDTH, BASE_HEIGHT)
                props.set_fixed_size(True)
                props.set_undecorated(False)  # Ensure proper OS window controls
                self.win.request_properties(props)

    def update(self, task):
        return task.cont

    def pause_game(self) -> None:
        if not self.paused:
            try:
                self.task_mgr.remove("update")
            except Exception as exc:
                logger.exception("Failed to pause game")
                raise
            else:
                self.paused = True

    def resume_game(self) -> None:
        if self.paused:
            try:
                self.task_mgr.add(self.update, "update")
            except Exception as exc:
                logger.exception("Failed to resume game")
                raise
            else:
                self.paused = False


def main() -> None:
    app = AutoFighterApp()
    app.run()


if __name__ == "__main__":
    main()
