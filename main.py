import logging

from panda3d.core import WindowProperties
from direct.showbase.ShowBase import ShowBase

from autofighter.menu import MainMenu
from autofighter.scene import SceneManager
from plugins.event_bus import EventBus
from plugins.plugin_loader import PluginLoader


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
            required=["player", "foe", "passive", "dot", "hot", "weapon", "room"],
        )
        self.plugin_loader.discover("plugins")
        self.plugin_loader.discover("mods")

        self.pause_on_stats = True
        self.stat_refresh_rate = 5
        self.paused = False

        props = WindowProperties()
        props.set_title("Midori AI AutoFighter")
        self.win.request_properties(props)

        self.accept("window-event", self.on_window_event)
        self.accept("escape", self.userExit)

        self.setBackgroundColor(0, 0, 0, 1)

        self._placeholder = self.loader.loadModel("models/box")
        self._placeholder.reparentTo(self.render)
        self._placeholder.setPos(0, 10, 0)
        logger.info("Placeholder model attached")

        self.task_mgr.add(self.update, "update")

        self.scene_manager.switch_to(MainMenu(self))

    def on_window_event(self, window) -> None:
        if window and window.is_closed():
            self.userExit()

    def update(self, task):
        return task.cont

    def pause_game(self) -> None:
        if not self.paused:
            try:
                self.task_mgr.remove("update")
            except Exception:
                pass
            self.paused = True

    def resume_game(self) -> None:
        if self.paused:
            try:
                self.task_mgr.add(self.update, "update")
            except Exception:
                pass
            self.paused = False


def main() -> None:
    app = AutoFighterApp()
    app.run()


if __name__ == "__main__":
    main()
