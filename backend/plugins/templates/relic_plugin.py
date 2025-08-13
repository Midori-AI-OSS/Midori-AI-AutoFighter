from dataclasses import dataclass
from dataclasses import field

from plugins.relics._base import RelicBase


@dataclass
class SampleRelic(RelicBase):
    id: str = "sample_relic"
    name: str = "Sample Relic"
    effects: dict[str, float] = field(default_factory=dict)
