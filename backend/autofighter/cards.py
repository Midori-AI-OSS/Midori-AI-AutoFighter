from __future__ import annotations

import random

from dataclasses import dataclass

from .party import Party


@dataclass(frozen=True)
class Card:
    id: str
    name: str
    stars: int
    effects: dict[str, float]

    def apply(self, party: Party) -> None:
        for member in party.members:
            for attr, pct in self.effects.items():
                if attr == "max_hp":
                    member.max_hp = type(member.max_hp)(member.max_hp * (1 + pct))
                    member.hp = type(member.hp)(member.hp * (1 + pct))
                else:
                    value = getattr(member, attr, None)
                    if value is None:
                        continue
                    new_value = type(value)(value * (1 + pct))
                    setattr(member, attr, new_value)


CARD_LIBRARY: dict[str, Card] = {
    "micro_blade": Card("micro_blade", "Micro Blade", 1, {"atk": 0.03}),
    "polished_shield": Card(
        "polished_shield", "Polished Shield", 1, {"defense": 0.03}
    ),
    "sturdy_vest": Card("sturdy_vest", "Sturdy Vest", 1, {"max_hp": 0.03}),
    "lucky_coin": Card("lucky_coin", "Lucky Coin", 1, {"crit_rate": 0.03}),
    "sharpening_stone": Card(
        "sharpening_stone", "Sharpening Stone", 1, {"crit_damage": 0.03}
    ),
    "mindful_tassel": Card(
        "mindful_tassel", "Mindful Tassel", 1, {"effect_hit_rate": 0.03}
    ),
    "calm_beads": Card("calm_beads", "Calm Beads", 1, {"effect_resistance": 0.03}),
    "balanced_diet": Card(
        "balanced_diet", "Balanced Diet", 1, {"max_hp": 0.03, "defense": 0.03}
    ),
}


def card_choices(party: Party, stars: int, count: int = 3) -> list[Card]:
    available = [
        c for c in CARD_LIBRARY.values() if c.stars == stars and c.id not in party.cards
    ]
    if not available:
        return []
    return random.sample(available, k=min(count, len(available)))


def award_card(party: Party, card_id: str) -> Card | None:
    card = CARD_LIBRARY.get(card_id)
    if card is None or card.id in party.cards:
        return None
    party.cards.append(card.id)
    return card


def apply_cards(party: Party) -> None:
    for cid in party.cards:
        card = CARD_LIBRARY.get(cid)
        if card:
            card.apply(party)
