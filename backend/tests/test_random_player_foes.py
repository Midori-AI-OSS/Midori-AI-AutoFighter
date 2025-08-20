import sys
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from plugins import players
from plugins import themedadj
from autofighter.party import Party
from plugins.players import Player
from autofighter.rooms import _choose_foe


def test_random_player_foes() -> None:
    random.seed(0)
    party = Party(members=[Player()])
    player_ids = {
        getattr(getattr(players, name), "id") for name in getattr(players, "__all__", [])
    }
    seen = [_choose_foe(party) for _ in range(20)]
    ids = {foe.id for foe in seen}
    assert any(fid in player_ids and fid != "slime" for fid in ids)
    player_foes = [foe for foe in seen if foe.id != "slime"]
    if player_foes:
        foe_name = player_foes[0].name
        assert any(adj.title() in foe_name for adj in themedadj.__all__)
