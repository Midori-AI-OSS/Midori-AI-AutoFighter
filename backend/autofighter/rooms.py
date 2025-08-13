from __future__ import annotations

import copy
import random

from typing import Any
from dataclasses import asdict
from dataclasses import fields
from dataclasses import dataclass

from .party import Party
from .stats import Stats
from .mapgen import MapNode
from plugins import foes as foe_plugins
from .passives import PassiveRegistry
from autofighter.cards import apply_cards
from autofighter.cards import card_choices
from autofighter.relics import apply_relics
from plugins.foes._base import FoeBase


def _scale_stats(obj: Stats, node: MapNode, strength: float = 1.0) -> None:
    mult = strength * node.floor * node.index * node.loop
    mult *= 1 + 0.05 * node.pressure
    for field in fields(type(obj)):
        value = getattr(obj, field.name, None)
        if isinstance(value, (int, float)):
            setattr(obj, field.name, type(value)(value * mult))


def _serialize(obj: Stats) -> dict[str, Any]:
    data = asdict(obj)
    data["id"] = obj.id
    if hasattr(obj, "name"):
        data["name"] = obj.name
    if hasattr(obj, "char_type"):
        data["char_type"] = getattr(obj.char_type, "value", obj.char_type)
    return data


def _choose_foe(party: Party) -> FoeBase:
    party_ids = {p.id for p in party.members}
    candidates = [
        getattr(foe_plugins, name)
        for name in getattr(foe_plugins, "__all__", [])
        if getattr(foe_plugins, name).id not in party_ids
    ]
    if not candidates:
        candidates = [foe_plugins.Slime]
    foe_cls = random.choice(candidates)
    return foe_cls()


@dataclass
class Room:
    node: MapNode

    def resolve(self, party: Party, data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


@dataclass
class BattleRoom(Room):
    def resolve(self, party: Party, data: dict[str, Any]) -> dict[str, Any]:
        registry = PassiveRegistry()
        foe = _choose_foe(party)
        _scale_stats(foe, self.node)
        combat_party = Party(
            members=[copy.deepcopy(m) for m in party.members],
            gold=party.gold,
            relics=party.relics,
            cards=party.cards,
        )
        apply_cards(combat_party)
        apply_relics(combat_party)
        for member, orig in zip(combat_party.members, party.members):
            registry.trigger("room_enter", member)
            registry.trigger("battle_start", member)
            foe.hp = max(foe.hp - member.atk, 0)
            member.apply_damage(foe.atk)
            orig.hp = min(member.hp, orig.max_hp)
        options = card_choices(party, stars=1)
        foes = [_serialize(foe)]
        party_data = [_serialize(p) for p in combat_party.members]
        choice_data = [
            {"id": c.id, "name": c.name, "stars": c.stars} for c in options
        ]
        return {
            "result": "battle",
            "party": party_data,
            "gold": party.gold,
            "relics": party.relics,
            "cards": party.cards,
            "card_choices": choice_data,
            "foes": foes,
        }


@dataclass
class BossRoom(BattleRoom):
    def resolve(self, party: Party, data: dict[str, Any]) -> dict[str, Any]:
        registry = PassiveRegistry()
        foe = _choose_foe(party)
        _scale_stats(foe, self.node, 100)
        combat_party = Party(
            members=[copy.deepcopy(m) for m in party.members],
            gold=party.gold,
            relics=party.relics,
            cards=party.cards,
        )
        apply_cards(combat_party)
        apply_relics(combat_party)
        for member, orig in zip(combat_party.members, party.members):
            registry.trigger("room_enter", member)
            registry.trigger("battle_start", member)
            foe.hp = max(foe.hp - member.atk, 0)
            member.apply_damage(foe.atk)
            orig.hp = min(member.hp, orig.max_hp)
        options = card_choices(party, stars=1)
        foes = [_serialize(foe)]
        party_data = [_serialize(p) for p in combat_party.members]
        choice_data = [
            {"id": c.id, "name": c.name, "stars": c.stars} for c in options
        ]
        return {
            "result": "boss",
            "party": party_data,
            "gold": party.gold,
            "relics": party.relics,
            "cards": party.cards,
            "card_choices": choice_data,
            "foes": foes,
        }


@dataclass
class ShopRoom(Room):
    def resolve(self, party: Party, data: dict[str, Any]) -> dict[str, Any]:
        registry = PassiveRegistry()
        heal = int(sum(m.max_hp for m in party.members) * 0.05)
        for member in party.members:
            registry.trigger("room_enter", member)
            member.apply_healing(heal)
        cost = int(data.get("cost", 0))
        item = data.get("item")
        if cost > 0 and party.gold >= cost:
            party.gold -= cost
            if item:
                party.relics.append(item)
        party_data = [_serialize(p) for p in party.members]
        return {
            "result": "shop",
            "party": party_data,
            "gold": party.gold,
            "relics": party.relics,
            "cards": party.cards,
            "card": None,
            "foes": [],
        }


@dataclass
class RestRoom(Room):
    def resolve(self, party: Party, data: dict[str, Any]) -> dict[str, Any]:
        registry = PassiveRegistry()
        for member in party.members:
            registry.trigger("room_enter", member)
            member.hp = member.max_hp
        party_data = [_serialize(p) for p in party.members]
        return {
            "result": "rest",
            "party": party_data,
            "gold": party.gold,
            "relics": party.relics,
            "cards": party.cards,
            "card": None,
            "foes": [],
        }


@dataclass
class ChatRoom(Room):
    def resolve(self, party: Party, data: dict[str, Any]) -> dict[str, Any]:
        registry = PassiveRegistry()
        for member in party.members:
            registry.trigger("room_enter", member)
        message = data.get("message", "")
        party_data = [_serialize(p) for p in party.members]
        return {
            "result": "chat",
            "message": message,
            "party": party_data,
            "gold": party.gold,
            "relics": party.relics,
            "cards": party.cards,
            "card": None,
            "foes": [],
        }

