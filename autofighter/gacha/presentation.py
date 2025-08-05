from __future__ import annotations

from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectLabel
from direct.showbase.ShowBase import ShowBase

from autofighter.gacha.crafting import trade_for_ticket
from autofighter.gacha.crafting import upgrade
from autofighter.gui import set_widget_pos


class CraftingPanel:
    """Simple UI for upgrade-item crafting."""

    def __init__(
        self,
        app: ShowBase,
        inventory: dict[int | str, int],
        *,
        on_close=None,
    ) -> None:
        self.app = app
        self.inventory = inventory
        self.on_close = on_close
        self.widgets: list[DirectButton | DirectFrame | DirectLabel] = []
        self.info_label: DirectLabel | None = None

    def setup(self) -> None:
        frame = DirectFrame(frameColor=(0, 0, 0, 0.5))
        set_widget_pos(frame, (0, 0, 0))
        self.widgets.append(frame)

        self.info_label = DirectLabel(
            text=self._info_text(),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(self.info_label, (0, 0, 0.6))
        self.widgets.append(self.info_label)

        up_button = DirectButton(
            text="Upgrade 1★",
            command=lambda: self._upgrade(1),
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(up_button, (0, 0, 0.2))
        trade_button = DirectButton(
            text="10×4★ → Ticket",
            command=self._trade,
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(trade_button, (0, 0, -0.2))
        close_button = DirectButton(
            text="Close",
            command=self.close,
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        set_widget_pos(close_button, (0, 0, -0.6))
        self.widgets.extend([up_button, trade_button, close_button])

    def _upgrade(self, star: int) -> None:
        if upgrade(self.inventory, star):
            self._refresh()

    def _trade(self) -> None:
        if trade_for_ticket(self.inventory):
            self._refresh()

    def _refresh(self) -> None:
        assert self.info_label is not None
        self.info_label["text"] = self._info_text()

    def _info_text(self) -> str:
        return (
            f"1★:{self.inventory.get(1,0)} "
            f"2★:{self.inventory.get(2,0)} "
            f"3★:{self.inventory.get(3,0)} "
            f"4★:{self.inventory.get(4,0)} "
            f"Tickets:{self.inventory.get('tickets',0)}"
        )

    def close(self) -> None:
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        if self.on_close:
            self.on_close()

