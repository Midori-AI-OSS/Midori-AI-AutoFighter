from __future__ import annotations

import time
import copy
import random
import math
import asyncio

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import fields
from typing import Any
from typing import Awaitable
from typing import Callable

from rich.console import Console

from .mapgen import MapNode
from .party import Party
from .passives import PassiveRegistry
from .stats import BUS
from .stats import Stats
from autofighter.cards import apply_cards
from autofighter.cards import card_choices
from autofighter.effects import EffectManager
from autofighter.relics import apply_relics
from autofighter.relics import relic_choices
from plugins import foes as foe_plugins
from plugins import players as player_plugins
from plugins.damage_types import ALL_DAMAGE_TYPES
from plugins.foes._base import FoeBase

ENRAGE_TURNS_NORMAL = 100
ENRAGE_TURNS_BOSS = 500

console = Console()

ELEMENTS = [e.lower() for e in ALL_DAMAGE_TYPES]


def _scale_stats(obj: Stats, node: MapNode, strength: float = 1.0) -> None:
    # Gentler growth across the run: small multiplicative bumps per axis
    starter_int = 1.0 + random.uniform(-0.05, 0.05)
    floor_mult = starter_int + 0.08 * max(node.floor - 1, 0)
    index_mult = starter_int + 0.10 * max(node.index - 1, 0)
    loop_mult = starter_int + 0.20 * max(node.loop - 1, 0)
    pressure_mult = 1.0 * max(node.pressure, 1) ## This is user controlled, do not change this...
    base_mult = max(strength * floor_mult * index_mult * loop_mult * pressure_mult, 0.5)

    # Apply a small per-room variation of +/-5% per stat to foes to avoid sameness.
    # Each numeric stat gets its own independent variation, applied once when the foe is created.
    for field in fields(type(obj)):
        if field.name in {"exp", "level", "exp_multiplier"}:
            continue
        value = getattr(obj, field.name, None)
        if isinstance(value, (int, float)):
            per_stat_variation = 1.0 + random.uniform(-0.05, 0.05)
            total = value * base_mult * per_stat_variation
            setattr(obj, field.name, type(value)(total))

    # Ensure foe level increases slowly with room progression (roughly every 2 rooms).
    try:
        room_num = max(int(node.index), 1)
        desired = max(1, math.ceil(room_num / 2))
        obj.level = int(max(getattr(obj, "level", 1), desired))
    except Exception:
        pass

    # Soften the HP floor: aim for ~700 × room with slight variance, not 1000 × room.
    try:
        room_num = max(int(node.index), 1)
        base_hp = 700 * room_num
        low = int(base_hp * 0.85)
        high = int(base_hp * 1.10)
        target = random.randint(low, max(high, low + 1))
        current_max = int(getattr(obj, "max_hp", 1))
        new_max = max(current_max, target)
        setattr(obj, "max_hp", new_max)
        setattr(obj, "hp", new_max)
    except Exception:
        pass

    # Safety: foes should never have crit_damage below 2.0 (i.e., +100%).
    try:
        cd = getattr(obj, "crit_damage", None)
        if isinstance(cd, (int, float)):
            setattr(obj, "crit_damage", type(cd)(max(float(cd), 2.0)))
    except Exception:
        pass

    # Reduce growth rate for high vitality values (foes only):
    # Beyond 2.0, slow progressively: every +0.25 over 2.0 increases the
    # slowdown by +1× starting from 5×. This preserves monotonic growth
    # without hard caps while increasingly compressing high values.
    try:
        if isinstance(obj, FoeBase):
            vit = getattr(obj, "vitality", None)
            if isinstance(vit, (int, float)):
                thr = 0.5
                step = 0.25
                base_slow = 5.0
                fvit = float(vit)
                if fvit > thr:
                    excess = fvit - thr
                    steps = int(excess // step)
                    factor = base_slow + steps
                    fvit = thr + (excess / factor)
                    fvit = max(fvit, 0.25)
                    setattr(obj, "vitality", type(vit)(fvit))
    except Exception:
        pass

    # Reduce growth rate for high mitigation values (foes only):
    # Beyond 2.0, slow progressively: every +0.1 over 2.0 increases the
    # slowdown by +1× starting from 5×.
    try:
        if isinstance(obj, FoeBase):
            mit = getattr(obj, "mitigation", None)
            if isinstance(mit, (int, float)):
                thr = 5
                step = 1
                base_slow = 5.0
                fmit = float(mit)
                if fmit > thr:
                    excess = fmit - thr
                    steps = int(excess // step)
                    factor = base_slow + steps
                    fmit = thr + (excess / factor)
                    fmit = max(fmit, 10)
                    setattr(obj, "mitigation", type(mit)(fmit))
    except Exception:
        pass


def _normalize_damage_type(dt: Any) -> str:
    # Always return a simple string identifier for damage type
    try:
        if isinstance(dt, str):
            return dt
        # dataclass instance or mapping from dataclass
        ident = getattr(dt, "id", None) or getattr(dt, "name", None)
        if ident:
            return str(ident)
        # mapping-like
        if isinstance(dt, dict):
            return str(dt.get("id") or dt.get("name") or "Generic")
    except Exception:
        pass
    return "Generic"


def _serialize(obj: Stats) -> dict[str, Any]:
    data = asdict(obj)
    norm = _normalize_damage_type(getattr(obj, "damage_type", None))
    data["damage_type"] = norm
    data["element"] = norm
    data["id"] = obj.id
    if hasattr(obj, "name"):
        data["name"] = obj.name
    if hasattr(obj, "char_type"):
        data["char_type"] = getattr(obj.char_type, "value", obj.char_type)
    return data


def _pick_card_stars(room: Room) -> int:
    roll = random.random()
    if isinstance(room, BossRoom):
        if roll < 0.60:
            return 3
        if roll < 0.85:
            return 4
        return 5
    if isinstance(room, BattleRoom) and room.strength > 1.0:
        if roll < 0.40:
            return 1
        if roll < 0.70:
            return 2
        if roll < 0.7015:
            return 3
        if roll < 0.7025:
            return 4
        return 5
    return 1 if roll < 0.80 else 2


def _roll_relic_drop(room: Room, rdr: float) -> bool:
    roll = random.random()
    base = 0.5 if isinstance(room, BossRoom) else 0.1
    return roll < min(base * rdr, 1.0)


def _pick_item_stars(room: Room) -> int:
    """Select an upgrade item star rank based on room difficulty.

    Star ranges come from the room-type tables: normal battles yield 1–2★
    items, bosses 1–3★, and floor bosses 3–4★. Floor, loop, and Pressure
    gradually raise the minimum within each band but the result never exceeds
    4★.
    """

    node = room.node
    if node.room_type == "battle-boss-floor":
        low, high = 3, 4
    elif isinstance(room, BossRoom) or getattr(room, "strength", 1.0) > 1.0:
        low, high = 1, 3
    else:
        low, high = 1, 2

    base = low + (node.floor - 1) // 20 + (node.loop - 1) + node.pressure // 10
    return min(base, high)


def _calc_gold(room: Room, rdr: float) -> int:
    node = room.node
    if node.room_type == "battle-boss-floor":
        base = 200
        mult = random.uniform(2.05, 4.25)
    elif isinstance(room, BossRoom) or getattr(room, "strength", 1.0) > 1.0:
        base = 20
        mult = random.uniform(1.53, 2.25)
    else:
        base = 5
        mult = random.uniform(1.01, 1.25)
    return int(base * node.loop * mult * rdr)


def _pick_relic_stars(room: Room) -> int:
    roll = random.random()
    if isinstance(room, BossRoom):
        if roll < 0.6:
            return 3
        if roll < 0.9:
            return 4
        return 5
    if roll < 0.7:
        return 1
    if roll < 0.9:
        return 2
    return 3


def _apply_rdr_to_stars(stars: int, rdr: float) -> int:
    """Chance to upgrade stars with extreme `rdr` values.

    Each extra star requires 1000× more `rdr` than the last. When `rdr` is
    at least 1000% (10×), a card or relic can roll to jump from 3★ to 4★. At
    1,000,000% (10 000×), it can try for 5★. The odds scale with `rdr` but are
    capped below certainty so lucky rolls are still required.
    """

    for threshold in (10.0, 10000.0):
        if stars >= 5 or rdr < threshold:
            break
        chance = min(rdr / (threshold * 10.0), 0.99)
        if random.random() < chance:
            stars += 1
        else:
            break
    return stars


def _choose_foe(party: Party) -> FoeBase:
    party_ids = {p.id for p in party.members}
    candidates = [
        getattr(foe_plugins, name)
        for name in getattr(foe_plugins, "__all__", [])
        if getattr(foe_plugins, name).id not in party_ids
    ]
    for name in getattr(player_plugins, "__all__", []):
        player_cls = getattr(player_plugins, name)
        if player_cls.id in party_ids:
            continue
        foe_cls = foe_plugins.PLAYER_FOES.get(player_cls.id)
        if foe_cls and foe_cls not in candidates:
            candidates.append(foe_cls)
    if not candidates:
        candidates = [foe_plugins.Slime]
    foe_cls = random.choice(candidates)
    foe = foe_cls()
    # Assign damage type to foes similar to players:
    # - If the foe's default is Generic or it's a Slime, roll a random element each encounter.
    # - If it is Luna, force Generic.
    # - Otherwise, keep the class-defined element (e.g., LadyOfFire stays Fire).
    try:
        label = str(getattr(foe, "name", None) or getattr(foe, "id", ""))

        def _as_str(t: object) -> str:
            try:
                if isinstance(t, str):
                    return t
                ident = getattr(t, "id", None) or getattr(t, "name", None)
                if ident:
                    return str(ident)
            except Exception:
                pass
            return "Generic"

        current = _as_str(getattr(foe, "damage_type", "Generic"))
        chosen: str | None = None
        low = label.lower()
        if "luna" in low:
            chosen = "Generic"
        elif "slime" in low or current.lower() == "generic":
            chosen = random.choice(ALL_DAMAGE_TYPES)
        # apply selection or normalize existing
        final = chosen or current
        foe.damage_type = final
        try:
            setattr(foe, "element", final)
        except Exception:
            pass
    except Exception:
        # Best-effort; leave default if anything goes wrong
        pass
    return foe


def _build_foes(node: MapNode, party: Party) -> list[FoeBase]:
    count = min(10, 1 + node.pressure // 5)
    return [_choose_foe(party) for _ in range(count)]


@dataclass
class Room:
    node: MapNode

    async def resolve(self, party: Party, data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


@dataclass
class BattleRoom(Room):
    strength: float = 1.0

    async def resolve(
        self,
        party: Party,
        data: dict[str, Any],
        progress: Callable[[dict[str, Any]], Awaitable[None]] | None = None,
        foe: Stats | list[Stats] | None = None,
    ) -> dict[str, Any]:
        registry = PassiveRegistry()
        start_gold = party.gold
        if foe is None:
            foes = _build_foes(self.node, party)
        else:
            foes = foe if isinstance(foe, list) else [foe]
        for f in foes:
            _scale_stats(f, self.node, self.strength)
        base_atks = [f.atk for f in foes]
        foe = foes[0]
        combat_party = Party(
            members=[copy.deepcopy(m) for m in party.members],
            gold=party.gold,
            relics=party.relics,
            cards=party.cards,
            rdr=party.rdr,
        )
        apply_cards(combat_party)
        apply_relics(combat_party)
        party.rdr = combat_party.rdr

        foe_effects = []
        for f in foes:
            mgr = EffectManager(f)
            f.effect_manager = mgr
            foe_effects.append(mgr)

        party_effects = []
        for member in combat_party.members:
            mgr = EffectManager(member)
            member.effect_manager = mgr
            party_effects.append(mgr)

        for f in foes:
            BUS.emit("battle_start", f)
            registry.trigger("battle_start", f)
        console.log(
            f"Battle start: {[f.id for f in foes]} vs {[m.id for m in combat_party.members]}"
        )
        for member_effect, member in zip(party_effects, combat_party.members):
            BUS.emit("battle_start", member)
            registry.trigger("battle_start", member)

        enrage_active = False
        enrage_stacks = 0
        enrage_bleed_applies = 0  # how many times we've applied enrage bleed
        threshold = ENRAGE_TURNS_BOSS if isinstance(self, BossRoom) else ENRAGE_TURNS_NORMAL
        exp_reward = 0
        turn = 0
        if progress is not None:
            await progress(
                {
                    "result": "battle",
                    "party": [_serialize(m) for m in combat_party.members],
                    "foes": [_serialize(f) for f in foes],
                    "enrage": {"active": False, "stacks": 0},
                    "rdr": party.rdr,
                }
            )
        while any(f.hp > 0 for f in foes) and any(
            m.hp > 0 for m in combat_party.members
        ):
            for member_effect, member in zip(party_effects, combat_party.members):
                if member.hp <= 0:
                    continue
                turn += 1
                if turn > threshold:
                    if not enrage_active:
                        enrage_active = True
                        for f in foes:
                            f.passives.append("Enraged")
                        console.log("Enrage activated")
                    enrage_stacks = turn - threshold
                    for i, f in enumerate(foes):
                        f.atk = int(base_atks[i] * (1 + 0.4 * enrage_stacks))
                turn_start = time.perf_counter()
                registry.trigger("turn_start", member)
                console.log(f"{member.id} turn start")
                await member.maybe_regain(turn)
                alive_foe_idxs = [i for i, f in enumerate(foes) if f.hp > 0]
                foe_idx = random.choice(alive_foe_idxs)
                foe = foes[foe_idx]
                foe_mgr = foe_effects[foe_idx]
                await member_effect.tick(foe_mgr)
                if member.hp <= 0:
                    registry.trigger("turn_end", member)
                    elapsed = time.perf_counter() - turn_start
                    if elapsed < 0.5:
                        await asyncio.sleep(0.5 - elapsed)
                    continue
                proceed = await member_effect.on_action()
                if proceed is None:
                    proceed = True
                # Ensure damage type object is instantiated before calling on_action
                try:
                    dt = getattr(member, "damage_type", None)
                    if isinstance(dt, str):
                        import importlib
                        module = importlib.import_module(
                            f"plugins.damage_types.{dt.lower()}"
                        )
                        member.damage_type = getattr(module, dt)()
                        dt = member.damage_type
                except Exception:
                    dt = getattr(member, "damage_type", None)
                if proceed and hasattr(dt, "on_action"):
                    res = await dt.on_action(
                        member,
                        combat_party.members,
                        foes,
                    )
                    if res is None:
                        proceed = True
                    else:
                        proceed = bool(res)
                if not proceed:
                    registry.trigger("turn_end", member)
                    if progress is not None:
                        await progress(
                            {
                                "result": "battle",
                                "party": [
                                _serialize(m) for m in combat_party.members
                                ],
                                "foes": [_serialize(f) for f in foes],
                                "enrage": {
                                    "active": enrage_active,
                                    "stacks": enrage_stacks,
                                },
                                "rdr": party.rdr,
                            }
                        )
                    elapsed = time.perf_counter() - turn_start
                    if elapsed < 0.5:
                        await asyncio.sleep(0.5 - elapsed)
                    continue
                dmg = await foe.apply_damage(member.atk, attacker=member)
                console.log(
                    f"[light_red]{member.id} hits {foe.id} for {dmg}[/]"
                )
                foe_mgr.maybe_inflict_dot(member, dmg)
                if getattr(member.damage_type, "id", "").lower() == "wind":
                    for extra_idx, extra_foe in enumerate(foes):
                        if extra_idx == foe_idx or extra_foe.hp <= 0:
                            continue
                        extra_dmg = await extra_foe.apply_damage(
                            member.atk, attacker=member
                        )
                        console.log(
                            f"[light_red]{member.id} hits {extra_foe.id} for {extra_dmg}[/]"
                        )
                        foe_effects[extra_idx].maybe_inflict_dot(member, extra_dmg)
                        if extra_foe.hp <= 0:
                            exp_reward += extra_foe.level * 12 + 5 * self.node.index
                            try:
                                label = (
                                    getattr(extra_foe, "name", None)
                                    or getattr(extra_foe, "id", "")
                                ).lower()
                                if "slime" in label:
                                    for m in combat_party.members:
                                        m.exp_multiplier += 0.025
                                    for m in party.members:
                                        m.exp_multiplier += 0.025
                            except Exception:
                                pass
                # Apply escalating enrage bleed every 10 enrage turns: add (1 + n) stacks
                # where n is the number of prior applications. Each stack lasts 10 turns.
                if enrage_active:
                    turns_since_enrage = max(enrage_stacks, 0)
                    next_trigger = (enrage_bleed_applies + 1) * 10
                    if turns_since_enrage >= next_trigger:
                        stacks_to_add = 1 + enrage_bleed_applies
                        from autofighter.effects import DamageOverTime
                        for mgr in party_effects:
                            for _ in range(stacks_to_add):
                                dmg_per_tick = int(max(mgr.stats.max_hp, 1) * 0.05)
                                mgr.add_dot(DamageOverTime("Enrage Bleed", dmg_per_tick, 10, "enrage_bleed"))
                        for mgr, foe_obj in zip(foe_effects, foes):
                            for _ in range(stacks_to_add):
                                dmg_per_tick = int(max(foe_obj.max_hp, 1) * 0.05)
                                mgr.add_dot(
                                    DamageOverTime(
                                        "Enrage Bleed", dmg_per_tick, 10, "enrage_bleed"
                                    )
                                )
                        enrage_bleed_applies += 1
                registry.trigger("turn_end", member)
                if progress is not None:
                    await progress(
                        {
                            "result": "battle",
                            "party": [_serialize(m) for m in combat_party.members],
                            "foes": [_serialize(f) for f in foes],
                            "enrage": {"active": enrage_active, "stacks": enrage_stacks},
                            "rdr": party.rdr,
                        }
                    )
                if foe.hp <= 0:
                    exp_reward += foe.level * 12 + 5 * self.node.index
                    # Slime kill bonus: grant +0.025 exp rate to all party members
                    try:
                        label = (getattr(foe, "name", None) or getattr(foe, "id", "")).lower()
                        if "slime" in label:
                            for m in combat_party.members:
                                m.exp_multiplier += 0.025
                            for m in party.members:
                                m.exp_multiplier += 0.025
                    except Exception:
                        pass
                    elapsed = time.perf_counter() - turn_start
                    if elapsed < 0.5:
                        await asyncio.sleep(0.5 - elapsed)
                    if all(f.hp <= 0 for f in foes):
                        break
                    continue
                # Foe targets a living party member weighted by DEF and mitigation
                alive = [
                    (idx, m)
                    for idx, m in enumerate(combat_party.members)
                    if m.hp > 0
                ]
                idx, target = random.choices(
                    alive,
                    weights=[m.defense * m.mitigation for _, m in alive],
                )[0]
                target_effect = party_effects[idx]
                registry.trigger("turn_start", foe)
                console.log(f"{foe.id} turn start targeting {target.id}")
                await foe.maybe_regain(turn)
                await foe_mgr.tick(target_effect)
                if foe.hp <= 0:
                    registry.trigger("turn_end", foe)
                    exp_reward += foe.level * 12 + 5 * self.node.index
                    # Slime kill bonus: grant +0.025 exp rate to all party members
                    try:
                        label = (getattr(foe, "name", None) or getattr(foe, "id", "")).lower()
                        if "slime" in label:
                            for m in combat_party.members:
                                m.exp_multiplier += 0.025
                            for m in party.members:
                                m.exp_multiplier += 0.025
                    except Exception:
                        pass
                    elapsed = time.perf_counter() - turn_start
                    if elapsed < 0.5:
                        await asyncio.sleep(0.5 - elapsed)
                    break
                proceed = await foe_mgr.on_action()
                if proceed is None:
                    proceed = True
                # Ensure foe damage type is instantiated before calling on_action
                try:
                    dt = getattr(foe, "damage_type", None)
                    if isinstance(dt, str):
                        import importlib
                        module = importlib.import_module(
                            f"plugins.damage_types.{dt.lower()}"
                        )
                        foe.damage_type = getattr(module, dt)()
                        dt = foe.damage_type
                except Exception:
                    dt = getattr(foe, "damage_type", None)
                if proceed and hasattr(dt, "on_action"):
                    res = await dt.on_action(
                        foe,
                        foes,
                        combat_party.members,
                    )
                    if res is None:
                        proceed = True
                    else:
                        proceed = bool(res)
                if not proceed:
                    registry.trigger("turn_end", foe)
                    if progress is not None:
                        await progress(
                            {
                                "result": "battle",
                                "party": [
                                    _serialize(m) for m in combat_party.members
                                ],
                                "foes": [_serialize(f) for f in foes],
                                "enrage": {
                                    "active": enrage_active,
                                    "stacks": enrage_stacks,
                                },
                                "rdr": party.rdr,
                            }
                        )
                    elapsed = time.perf_counter() - turn_start
                    if elapsed < 0.5:
                        await asyncio.sleep(0.5 - elapsed)
                    continue
                dmg = await target.apply_damage(foe.atk, attacker=foe)
                console.log(
                    f"[light_red]{foe.id} hits {target.id} for {dmg}[/]"
                )
                target_effect.maybe_inflict_dot(foe, dmg)
                if getattr(foe.damage_type, "id", "").lower() == "wind":
                    for extra_mgr, extra_member in zip(
                        party_effects, combat_party.members
                    ):
                        if extra_member is target or extra_member.hp <= 0:
                            continue
                        extra_dmg = await extra_member.apply_damage(
                            foe.atk, attacker=foe
                        )
                        console.log(
                            f"[light_red]{foe.id} hits {extra_member.id} for {extra_dmg}[/]"
                        )
                        extra_mgr.maybe_inflict_dot(foe, extra_dmg)
                registry.trigger("turn_end", foe)
                if progress is not None:
                    await progress(
                        {
                            "result": "battle",
                            "party": [_serialize(m) for m in combat_party.members],
                            "foes": [_serialize(f) for f in foes],
                            "enrage": {"active": enrage_active, "stacks": enrage_stacks},
                            "rdr": party.rdr,
                        }
                    )
                elapsed = time.perf_counter() - turn_start
                if elapsed < 0.5:
                    await asyncio.sleep(0.5 - elapsed)
            else:
                continue
            break
            
        # Determine outcome before distributing rewards
        party_alive = any(m.hp > 0 for m in combat_party.members)
        foe_alive = any(f.hp > 0 for f in foes)
        for f in foes:
            registry.trigger("battle_end", f)
        console.log("Battle end")
        for member in combat_party.members:
            BUS.emit("battle_end", member)
            registry.trigger("battle_end", member)
        # On defeat, skip rewards and end the run cleanly after returning the snapshot
        if not party_alive and foe_alive:
            foes_data = [_serialize(f) for f in foes]
            party_data = [_serialize(p) for p in combat_party.members]
            # Ensure original party reflects current HP lost
            for member, orig in zip(combat_party.members, party.members):
                orig.hp = min(member.hp, orig.max_hp)
            return {
                "result": "defeat",
                "party": party_data,
                "gold": party.gold,
                "relics": party.relics,
                "cards": party.cards,
                "card_choices": [],
                "relic_choices": [],
                # Provide an empty loot object so the frontend poll stops without showing RewardOverlay
                "loot": {"gold": 0, "items": []},
                "foes": foes_data,
                "room_number": self.node.index,
                "exp_reward": 0,
                "enrage": {"active": enrage_active, "stacks": enrage_stacks},
                "rdr": party.rdr,
            }

        for member, orig in zip(combat_party.members, party.members):
            orig.gain_exp(exp_reward)
            orig.hp = min(member.hp, orig.max_hp)
            for f in fields(type(orig)):
                setattr(member, f.name, getattr(orig, f.name))

        card_stars = _pick_card_stars(self)
        card_stars = _apply_rdr_to_stars(card_stars, party.rdr)
        options = card_choices(party, stars=card_stars)
        relic_opts = []
        if _roll_relic_drop(self, party.rdr):
            rstars = _pick_relic_stars(self)
            rstars = _apply_rdr_to_stars(rstars, party.rdr)
            relic_opts = relic_choices(party, stars=rstars)
        foes_data = [_serialize(f) for f in foes]
        party_data = [_serialize(p) for p in combat_party.members]
        choice_data = [
            {
                "id": c.id,
                "name": c.name,
                "stars": c.stars,
                "about": getattr(c, "about", ""),
            }
            for c in options
        ]
        relic_choice_data = [
            {"id": r.id, "name": r.name, "stars": r.stars} for r in relic_opts
        ]
        gold_reward = _calc_gold(self, party.rdr)
        party.gold += gold_reward
        BUS.emit("gold_earned", gold_reward)
        # Rare drop rate multiplies the number of element upgrade items but
        # never their star rank.
        item_base = 1 * party.rdr
        base_int = int(item_base)
        item_count = max(1, base_int)
        if random.random() < item_base - base_int:
            item_count += 1
        items = [
            {"id": random.choice(ELEMENTS), "stars": _pick_item_stars(self)}
            for _ in range(item_count)
        ]
        ticket_chance = 0.1 * party.rdr
        if random.random() < ticket_chance:
            items.append({"id": "ticket", "stars": 0})
        loot = {
            "gold": party.gold - start_gold,
            "card_choices": choice_data,
            "relic_choices": relic_choice_data,
            "items": items,
        }
        return {
            "result": "boss" if self.strength > 1.0 else "battle",
            "party": party_data,
            "gold": party.gold,
            "relics": party.relics,
            "cards": party.cards,
            "card_choices": choice_data,
            "relic_choices": relic_choice_data,
            "loot": loot,
            "foes": foes_data,
            "room_number": self.node.index,
            "exp_reward": exp_reward,
            "enrage": {"active": enrage_active, "stacks": enrage_stacks},
            "rdr": party.rdr,
        }


@dataclass
class BossRoom(BattleRoom):
    strength: float = 100.0


@dataclass
class ShopRoom(Room):
    async def resolve(self, party: Party, data: dict[str, Any]) -> dict[str, Any]:
        registry = PassiveRegistry()
        heal = int(sum(m.max_hp for m in party.members) * 0.05)
        for member in party.members:
            registry.trigger("room_enter", member)
            await member.apply_healing(heal)
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
            "rdr": party.rdr,
            "card": None,
            "foes": [],
        }


@dataclass
class RestRoom(Room):
    async def resolve(self, party: Party, data: dict[str, Any]) -> dict[str, Any]:
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
            "rdr": party.rdr,
            "card": None,
            "foes": [],
        }


@dataclass
class ChatRoom(Room):
    async def resolve(self, party: Party, data: dict[str, Any]) -> dict[str, Any]:
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
            "rdr": party.rdr,
            "card": None,
            "foes": [],
        }
