"""Main menu rebuilt with Panda3D DirectGUI elements."""

from __future__ import annotations

import random
from pathlib import Path

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath

from autofighter.save import DB_PATH
from autofighter.saves import SaveManager


class MainMenu:
    """Basic main menu layout with top bar and icon grid."""

    def __init__(
        self,
        parent: NodePath,
        app: object | None = None,
        *,
        has_run: bool = False,
        db_path: Path | str = DB_PATH,
        avatars_dir: Path | str = Path("assets/textures/players"),
    ) -> None:
        self.app = app
        self.root = DirectFrame(parent=parent)

        self.top_bar = DirectFrame(parent=self.root)
        avatar_path = self._ensure_avatar(Path(db_path), Path(avatars_dir))
        self.avatar = DirectFrame(
            parent=self.top_bar,
            frameSize=(0, 0.28, 0, 0.28),
            image=str(avatar_path) if avatar_path else None,
        )
        self.name_label = DirectButton(parent=self.top_bar, text="Player")
        self.pull_label = DirectButton(parent=self.top_bar, text="0")
        self.banner = DirectFrame(parent=self.top_bar)

        self.run_button = DirectButton(
            parent=self.root,
            text="Load Run" if has_run else "Start Run",
            command=self.load_run if has_run else self.start_run,
        )
        self.icon_buttons: list[DirectButton] = [self.run_button]
        for label, command in (
            ("Edit Player", self.edit_player),
            ("Edit Party", self.edit_party),
            ("Pull Characters", self.pull_characters),
            ("Options", self.options),
            ("Give Feedback", self.give_feedback),
            ("Quit", self.quit),
        ):
            button = DirectButton(parent=self.root, text=label, command=command)
            self.icon_buttons.append(button)

    def _ensure_avatar(self, db_path: Path, avatars_dir: Path) -> Path | None:
        try:
            with SaveManager(db_path, "") as sm:
                data = sm.fetch_player("player") or {}
                avatar_str = data.get("avatar")
                if avatar_str:
                    avatar_path = Path(avatar_str)
                    if avatar_path.exists():
                        return avatar_path
                candidates = [
                    p
                    for p in avatars_dir.glob("*")
                    if p.suffix.lower() in {".png", ".jpg", ".jpeg"}
                ]
                if not candidates:
                    return None
                avatar_path = random.choice(candidates)
                data["avatar"] = str(avatar_path)
                sm.queue_player("player", data)
                sm.commit()
                return avatar_path
        except Exception:
            return None

    # Stub actions
    def start_run(self) -> None:
        """Launch a placeholder run map."""
        if self.app is None:  # pragma: no cover - safeguard
            return
        from autofighter.stats import Stats
        from game.ui.run_map import RunMap

        run_map = RunMap(self.app, Stats(hp=1, max_hp=1), [], Path("used_seeds.json"))
        self.app.scene_manager.switch_to(run_map)

    def load_run(self) -> None:  # pragma: no cover - placeholders
        pass

    def edit_player(self) -> None:  # pragma: no cover - placeholders
        pass

    def edit_party(self) -> None:  # pragma: no cover - placeholders
        pass

    def pull_characters(self) -> None:  # pragma: no cover - placeholders
        pass

    def options(self) -> None:  # pragma: no cover - placeholders
        pass

    def give_feedback(self) -> None:  # pragma: no cover - placeholders
        pass

    def quit(self) -> None:  # pragma: no cover - placeholders
        pass
