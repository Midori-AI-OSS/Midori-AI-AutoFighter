import pytest

from autofighter.gacha import GachaSystem, Pity


def test_pity_chance_scaling() -> None:
    pity = Pity()
    assert pity.chance() == pytest.approx(0.00001)

    for _ in range(158):
        pity.record_pull(False)
    assert pity.chance() == pytest.approx(0.05, rel=1e-3)

    for _ in range(21):
        pity.record_pull(False)
    assert pity.chance() == 1.0

    pity.record_pull(True)
    assert pity.chance() == pytest.approx(0.00001)
    assert pity.pulls_without_featured == 0


def test_gacha_system_pity_state() -> None:
    gacha = GachaSystem()
    assert gacha.pity_count() == 0
    assert gacha.pity_chance() == pytest.approx(Pity.base_rate)

    gacha.pull(False)
    assert gacha.pity_count() == 1
    assert gacha.pity_chance() > Pity.base_rate

    gacha.pull(True)
    assert gacha.pity_count() == 0
    assert gacha.pity_chance() == pytest.approx(Pity.base_rate)
