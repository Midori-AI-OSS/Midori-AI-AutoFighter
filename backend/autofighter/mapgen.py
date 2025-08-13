from __future__ import annotations

from dataclasses import dataclass, asdict
from random import Random
from typing import ClassVar


@dataclass
class MapNode:
    room_id: int
    room_type: str
    floor: int
    index: int
    loop: int
    pressure: int

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "MapNode":
        return cls(**data)


class MapGenerator:
    rooms_per_floor: ClassVar[int] = 45

    def __init__(self, seed: str, floor: int = 1, loop: int = 1, pressure: int = 0) -> None:
        self._rand = Random(seed)
        self.floor = floor
        self.loop = loop
        self.pressure = pressure

    def generate_floor(self) -> list[MapNode]:
        nodes: list[MapNode] = []
        index = 0
        nodes.append(
            MapNode(
                room_id=index,
                room_type="start",
                floor=self.floor,
                index=index,
                loop=self.loop,
                pressure=self.pressure,
            )
        )
        index += 1
        middle = self.rooms_per_floor - 2
        quotas = {"shop": 2, "rest": 2}
        room_types: list[str] = []
        for key, count in quotas.items():
            room_types.extend([key] * count)
        battle_count = middle - sum(quotas.values())
        weak = battle_count // 2
        normal = battle_count - weak
        room_types.extend(["battle-weak"] * weak)
        room_types.extend(["battle-normal"] * normal)
        self._rand.shuffle(room_types)
        for rt in room_types:
            nodes.append(
                MapNode(
                    room_id=index,
                    room_type=rt,
                    floor=self.floor,
                    index=index,
                    loop=self.loop,
                    pressure=self.pressure,
                )
            )
            index += 1
        nodes.append(
            MapNode(
                room_id=index,
                room_type="battle-boss-floor",
                floor=self.floor,
                index=index,
                loop=self.loop,
                pressure=self.pressure,
            )
        )
        return nodes
