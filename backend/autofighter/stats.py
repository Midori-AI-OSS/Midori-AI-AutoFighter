import importlib
import random

from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from typing import Callable
from typing import Optional

from rich.console import Console

from plugins.event_bus import EventBus
from plugins.damage_types.generic import Generic
from plugins.damage_types._base import DamageTypeBase

@dataclass
class Stats:
    hp: int = 1000
    max_hp: int = 1000
    exp: int = 0
    level: int = 1
    exp_multiplier: float = 1.0
    actions_per_turn: int = 1

    atk: int = 200
    crit_rate: float = 0.05
    crit_damage: float = 2.0
    effect_hit_rate: float = 1.0
    base_damage_type: DamageTypeBase = field(default_factory=Generic)

    defense: int = 200
    mitigation: float = 1.0
    regain: int = 100
    dodge_odds: float = 0.05
    effect_resistance: float = 0.05

    vitality: float = 1.0
    action_points: int = 0
    damage_taken: int = 0
    damage_dealt: int = 0
    kills: int = 0

    last_damage_taken: int = 0

    passives: list[str] = field(default_factory=list)
    dots: list[str] = field(default_factory=list)
    hots: list[str] = field(default_factory=list)
    damage_types: list[str] = field(default_factory=list)

    def exp_to_level(self) -> int:
        return (2 ** self.level) * 50

    async def maybe_regain(self, turn: int) -> None:
        if turn % 2 != 0:
            return
        bonus = max(self.regain - 100, 0) * 0.00005
        percent = 0.01 + bonus
        heal = int(self.max_hp * percent)
        await self.apply_healing(heal)

    def _on_level_up(self) -> None:
        inc = random.uniform(0.003 * self.level, 0.008 * self.level)
        for f in fields(type(self)):
            if f.name in {"exp", "level", "vitality", "exp_multiplier"}:
                continue
            value = getattr(self, f.name, None)
            if isinstance(value, (int, float)):
                new_val = value * (1 + inc)
                setattr(self, f.name, type(value)(new_val))
        self.max_hp += 10 * self.level
        self.hp = self.max_hp
        self.atk += 5 * self.level
        self.defense += 3 * self.level

    def gain_exp(self, amount: int) -> None:
        self.exp += int(amount * self.exp_multiplier * self.vitality)
        while self.exp >= self.exp_to_level():
            needed = self.exp_to_level()
            self.exp -= needed
            self.level += 1
            self._on_level_up()

    async def apply_damage(self, amount: int, attacker: Optional["Stats"] = None) -> int:
        def _ensure(obj: "Stats") -> DamageTypeBase:
            dt = getattr(obj, "base_damage_type", Generic())
            if isinstance(dt, str):
                module = importlib.import_module(f"plugins.damage_types.{dt.lower()}")
                dt = getattr(module, dt)()
                obj.base_damage_type = dt
            return dt

        if attacker is not None:
            atk_type = _ensure(attacker)
            atk_type.on_hit(attacker, self)
            amount = atk_type.on_damage(amount, attacker, self)
        self_type = _ensure(self)
        amount = self_type.on_damage_taken(amount, attacker, self)
        amount = self_type.on_party_damage_taken(amount, attacker, self)
        src_vit = attacker.vitality if attacker is not None else 1.0
        defense_term = max(self.defense ** 5, 1)
        amount = ((amount ** 2) * src_vit) / (defense_term * self.vitality * self.mitigation)
        amount = max(int(amount), 1)
        self.last_damage_taken = amount
        self.damage_taken += amount
        self.hp = max(self.hp - amount, 0)
        BUS.emit("damage_taken", self, attacker, amount)
        if attacker is not None:
            attacker.damage_dealt += amount
            BUS.emit("damage_dealt", attacker, self, amount)
        return amount

    async def apply_healing(self, amount: int, healer: Optional["Stats"] = None) -> int:
        def _ensure(obj: "Stats") -> DamageTypeBase:
            dt = getattr(obj, "base_damage_type", Generic())
            if isinstance(dt, str):
                module = importlib.import_module(f"plugins.damage_types.{dt.lower()}")
                dt = getattr(module, dt)()
                obj.base_damage_type = dt
            return dt

        if healer is not None:
            heal_type = _ensure(healer)
            amount = heal_type.on_heal(amount, healer, self)
        self_type = _ensure(self)
        amount = self_type.on_heal_received(amount, healer, self)
        src_vit = healer.vitality if healer is not None else 1.0
        # Healing is amplified by both source and target vitality
        amount = int(amount * src_vit * self.vitality)
        self.hp = min(self.hp + amount, self.max_hp)
        BUS.emit("heal_received", self, healer, amount)
        if healer is not None:
            BUS.emit("heal", healer, self, amount)
        return amount


StatusHook = Callable[["Stats"], None]
STATUS_HOOKS: list[StatusHook] = []
BUS = EventBus()

console = Console()


def _log_damage_taken(
    target: "Stats", attacker: Optional["Stats"], amount: int
) -> None:
    attacker_id = getattr(attacker, "id", "unknown")
    console.log(
        f"[light_red]{target.id} takes {amount} from {attacker_id}[/]"
    )


def _log_heal_received(
    target: "Stats", healer: Optional["Stats"], amount: int
) -> None:
    healer_id = getattr(healer, "id", "unknown")
    console.log(f"[green]{target.id} heals {amount} from {healer_id}[/]")


BUS.subscribe("damage_taken", _log_damage_taken)
BUS.subscribe("heal_received", _log_heal_received)


def add_status_hook(hook: StatusHook) -> None:
    STATUS_HOOKS.append(hook)


def apply_status_hooks(stats: "Stats") -> None:
    for hook in STATUS_HOOKS:
        hook(stats)
