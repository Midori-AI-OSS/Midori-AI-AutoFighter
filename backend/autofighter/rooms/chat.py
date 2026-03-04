from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..party import Party
from ..passives import PassiveRegistry
from . import Room
from .utils import _serialize


@dataclass
class ChatRoom(Room):
    """Chat rooms echo input while LRM integration is disabled."""

    async def resolve(self, party: Party, data: dict[str, Any]) -> dict[str, Any]:
        registry = PassiveRegistry()
        for member in party.members:
            await registry.trigger("room_enter", member)
        message = data.get("message", "")
        party_data = [_serialize(p) for p in party.members]
        reply = ""
        return {
            "result": "chat",
            "message": message,
            "response": reply,
            "voice": None,
            "party": party_data,
            "gold": party.gold,
            "relics": party.relics,
            "cards": party.cards,
            "rdr": party.rdr,
            "card": None,
            "foes": [],
        }
