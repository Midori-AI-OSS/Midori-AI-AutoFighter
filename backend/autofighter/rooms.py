from __future__ import annotations

import random
from dataclasses import dataclass
from dataclasses import asdict
from dataclasses import fields
from typing import Any

from plugins import players as player_plugins
from plugins.players._base import PlayerBase

from .mapgen import MapNode
from .passives import PassiveRegistry


def _scale_stats(obj: PlayerBase, node: MapNode, strength: float = 0.1) -> None:
    mult = strength * node.floor * node.index * node.loop
    mult *= 1 + 0.05 * node.pressure
    for field in fields(PlayerBase):
        value = getattr(obj, field.name, None)
        if isinstance(value, (int, float)):
            setattr(obj, field.name, type(value)(value * mult))


def _serialize(obj: PlayerBase) -> dict[str, Any]:
    data = asdict(obj)
    data["id"] = obj.id
    if hasattr(obj, "name"):
        data["name"] = obj.name
    if hasattr(obj, "char_type"):
        data["char_type"] = getattr(obj.char_type, "value", obj.char_type)
    return data


def _choose_foe(party: list[PlayerBase]) -> PlayerBase:
    party_ids = {p.id for p in party}
    candidates = [
        getattr(player_plugins, name)
        for name in getattr(player_plugins, "__all__", [])
        if getattr(player_plugins, name).id not in party_ids
    ]
    if not candidates:
        candidates = [player_plugins.Player]
    foe_cls = random.choice(candidates)
    return foe_cls()


@dataclass
class Room:
    node: MapNode

    def resolve(self, party: list[PlayerBase], data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


@dataclass
class BattleRoom(Room):
    def resolve(self, party: list[PlayerBase], data: dict[str, Any]) -> dict[str, Any]:
        registry = PassiveRegistry()
        foe = _choose_foe(party)
        _scale_stats(foe, self.node, 0.1)
        for member in party:
            registry.trigger("room_enter", member)
            registry.trigger("battle_start", member)
            foe.hp = max(foe.hp - member.atk, 0)
            member.apply_damage(foe.atk)
        foes = [_serialize(foe)]
        party_data = [_serialize(p) for p in party]
        return {"result": "battle", "party": party_data, "foes": foes}


@dataclass
class BossRoom(BattleRoom):
    def resolve(self, party: list[PlayerBase], data: dict[str, Any]) -> dict[str, Any]:
        registry = PassiveRegistry()
        foe = _choose_foe(party)
        _scale_stats(foe, self.node, 0.5)
        for member in party:
            registry.trigger("room_enter", member)
            registry.trigger("battle_start", member)
            foe.hp = max(foe.hp - member.atk, 0)
            member.apply_damage(foe.atk)
        foes = [_serialize(foe)]
        party_data = [_serialize(p) for p in party]
        return {"result": "boss", "party": party_data, "foes": foes}


@dataclass
class ShopRoom(Room):
    def resolve(self, party: list[PlayerBase], data: dict[str, Any]) -> dict[str, Any]:
        registry = PassiveRegistry()
        for member in party:
            registry.trigger("room_enter", member)
        cost = int(data.get("cost", 0))
        item = data.get("item")
        total_gold = sum(p.gold for p in party)
        if cost > 0 and total_gold >= cost:
            remaining = cost
            for member in party:
                if remaining == 0:
                    break
                deduction = min(member.gold, remaining)
                member.gold -= deduction
                remaining -= deduction
            if item and party:
                party[0].relics.append(item)
        party_data = [_serialize(p) for p in party]
        return {"result": "shop", "party": party_data, "foes": []}


@dataclass
class RestRoom(Room):
    def resolve(self, party: list[PlayerBase], data: dict[str, Any]) -> dict[str, Any]:
        registry = PassiveRegistry()
        for member in party:
            registry.trigger("room_enter", member)
            member.hp = member.max_hp
        party_data = [_serialize(p) for p in party]
        return {"result": "rest", "party": party_data, "foes": []}


@dataclass
class ChatRoom(Room):
    def resolve(self, party: list[PlayerBase], data: dict[str, Any]) -> dict[str, Any]:
        registry = PassiveRegistry()
        for member in party:
            registry.trigger("room_enter", member)
        message = data.get("message", "")
        party_data = [_serialize(p) for p in party]
        return {"result": "chat", "message": message, "party": party_data, "foes": []}

