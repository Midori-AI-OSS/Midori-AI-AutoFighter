from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from services import lrm_service

from ..party import Party
from ..passives import PassiveRegistry
from . import Room
from .utils import _serialize


@dataclass
class ChatRoom(Room):
    """Chat rooms return one-shot replies when the LRM provider is enabled."""

    async def resolve(self, party: Party, data: dict[str, Any]) -> dict[str, Any]:
        registry = PassiveRegistry()
        for member in party.members:
            await registry.trigger("room_enter", member)
        message = data.get("message", "")
        party_data = [_serialize(p) for p in party.members]
        reply = await lrm_service.generate_chat_reply(str(message), party_data)
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
