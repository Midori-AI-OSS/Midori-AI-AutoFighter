from __future__ import annotations

from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectLabel
from direct.showbase.ShowBase import ShowBase

from autofighter.gacha.crafting import FOUR_STAR_ITEM
from autofighter.gacha.crafting import TICKET_ITEM
from autofighter.gacha.crafting import trade_items_for_ticket
from autofighter.gui import set_widget_pos
from autofighter.scene import Scene


class GachaMenu(Scene):
    """Basic gacha UI with a trade option."""

    def __init__(
        self,
        app: ShowBase,
        return_scene_factory,
        *,
        inventory: dict[str, int] | None = None,
    ) -> None:
        self.app = app
        self.return_scene_factory = return_scene_factory
        self.inventory = inventory or {}
        self.widgets: list[DirectButton | DirectLabel] = []
        self.info_label: DirectLabel | None = None

    def setup(self) -> None:
        self.info_label = DirectLabel(
            text=self._info_text(),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(self.info_label, (0, 0, 0.7))
        trade_button = DirectButton(
            text="Trade 10x4★ for Ticket",
            command=self.trade,
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(trade_button, (0, 0, 0))
        leave_button = DirectButton(
            text="Leave",
            command=self.exit,
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(leave_button, (0.3, 0, -0.7))
        self.widgets.extend([self.info_label, trade_button, leave_button])
        self.app.accept("escape", self.exit)

    def teardown(self) -> None:
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        self.app.ignore("escape")

    def trade(self) -> None:
        trade_items_for_ticket(self.inventory)
        self._update_info()

    def _update_info(self) -> None:
        assert self.info_label is not None
        self.info_label["text"] = self._info_text()

    def _info_text(self) -> str:
        return (
            f"4★ Items: {self.inventory.get(FOUR_STAR_ITEM, 0)}\n"
            f"Tickets: {self.inventory.get(TICKET_ITEM, 0)}"
        )

    def exit(self) -> None:
        self.app.scene_manager.switch_to(self.return_scene_factory())
