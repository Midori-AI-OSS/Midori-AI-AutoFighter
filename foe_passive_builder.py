
#themed_ajt = ["atrocious", "baneful", "barbaric", "beastly", "belligerent", "bloodthirsty", "brutal", "callous", "cannibalistic", "cowardly", "cruel", "cunning", "dangerous", "demonic", "depraved", "destructive", "diabolical", "disgusting", "dishonorable", "dreadful", "eerie", "evil", "execrable", "fiendish", "filthy", "foul", "frightening", "ghastly", "ghoulish", "gruesome", "heinous", "hideous", "homicidal", "horrible", "hostile", "inhumane", "insidious", "intimidating", "malevolent", "malicious", "monstrous", "murderous", "nasty", "nefarious", "noxious", "obscene", "odious", "ominous", "pernicious", "perverted", "poisonous", "predatory", "premeditated", "primal", "primitive", "profane", "psychopathic", "rabid", "relentless", "repulsive", "ruthless", "sadistic", "savage", "scary", "sinister", "sociopathic", "spiteful", "squalid", "terrifying", "threatening", "treacherous", "ugly", "unholy", "venomous", "vicious", "villainous", "violent", "wicked", "wrongful", "xenophobic"]
#themed_names = ["luna", "carly", "becca", "ally", "hilander", "chibi", "mimic", "mezzy", "graygray", "bubbles"]

from __future__ import annotations

import random

from typing import TYPE_CHECKING

from themedstuff import themed_ajt
from themedstuff import themed_names

if TYPE_CHECKING:
    from player import Player


def player_stat_picker(player: Player) -> int:
    """Return a random stat tier based on the player's themed name."""
    if themed_names[0] in player.PlayerName.lower():
        return random.choice([5, 6, 7, 9])

    if themed_names[1] in player.PlayerName.lower():
        return random.choice([2, 2, 2, 2, 2, 2, 2, 2, 9])
        
    if themed_names[2] in player.PlayerName.lower():
        return random.choice([1, 3, 5, 6, 9])

    if themed_names[3] in player.PlayerName.lower():
        return random.choice([1, 2, 3, 9])

    if themed_names[4] in player.PlayerName.lower():
        return random.choice([6, 6, 6, 6, 6, 6, 9])

    if themed_names[5] in player.PlayerName.lower():
        return 9

    if themed_names[6] in player.PlayerName.lower():
        return 9

    if themed_names[7] in player.PlayerName.lower():
        return random.choice([1, 9])

    if themed_names[8] in player.PlayerName.lower():
        return random.choice([4, 9])

    if themed_names[9] in player.PlayerName.lower():
        return random.choice([8, 9])

    return 9


def build_foe_stats(player: Player) -> None:
    """Apply passive bonuses based on player traits."""
    _apply_high_level_lady(player)
    _apply_themed_name_modifiers(player)
    _apply_themed_adj_modifiers(player)



def _apply_high_level_lady(player: Player) -> None:
    if player.level > 2500:
        if "lady" in player.PlayerName.lower():

            if "light" in player.PlayerName.lower():
                player.Regain *= 2
                player.Mitigation += 4
                player.Vitality *= 1.5

            if "dark" in player.PlayerName.lower():
                player.Regain /= 2
                player.Mitigation /= 5
                player.Vitality *= 2.5

            if "fire" in player.PlayerName.lower():
                player.Regain /= 2
                player.Mitigation *= 2
                player.Atk *= 4

            if "ice" in player.PlayerName.lower():
                player.Regain *= 2
                player.Mitigation *= 5
                player.Vitality *= 2.5

            player.MHP *= 10
            player.Atk *= 2
            player.Def *= 2
            player.Mitigation = max(player.Mitigation, 1)
            player.Vitality *= 1.5
            player.EffectRES += 2


def _apply_themed_name_modifiers(player: Player) -> None:
    if themed_names[0] in player.PlayerName.lower():
        dodge_buff = 0.35
        max_hp_debuff = player.MHP / 4

        while player.MHP > max_hp_debuff:
            dodge_buff = dodge_buff + (0.001 * player.Vitality)
            player.MHP = player.MHP - 1

        player.Atk = int(player.Atk * 1)
        player.Def = int(player.Def * 2)
        player.gain_crit_rate(0.00001 * player.level)
        player.DodgeOdds += dodge_buff * player.Vitality

    if themed_names[1] in player.PlayerName.lower():
        def_to_add = 10000

        player.MHP *= 10
        player.Mitigation *= 10
        player.EffectRES += 255

        max_hp_debuff = max(player.MHP - random.randint(5 * player.level, 15 * player.level), 10)
        max_crit_rate = player.CritRate / 100
        max_atk_stat = round(player.Atk * 0.95)
        item_buff = random.uniform(0.4, 0.9)

        while player.Vitality > max(0.2, player.Vitality / player.level):
            item_buff += random.uniform(0.01, 0.3)
            player.Vitality = player.Vitality - 0.001

        while player.MHP > max_hp_debuff:
            player.Def += player.check_base_stats(player.Def, def_to_add)
            player.MHP = player.MHP - 1

        while player.CritRate > max_crit_rate:
            player.Def += player.check_base_stats(player.Def, def_to_add)
            player.CritRate -= player.CritRate / 15

        while player.Atk > max_atk_stat:
            player.Def += player.check_base_stats(player.Def, def_to_add)
            player.Atk = player.Atk - 1

        while player.Regain > 5:
            player.Def += player.check_base_stats(player.Def, def_to_add)
            player.Regain = player.Regain - 0.001

        player.Atk = int(player.Atk) + 1
        player.Def += player.check_base_stats(player.Def, int(player.Def * player.level) + 1)

        player.gain_crit_damage((0.0002 * player.level))

        while player.Def > 25000:
            item_buff += random.uniform(0.05, 0.25)
            player.Def = player.Def - 5
        
        for item in player.Items:
            item.name = "Carly\'s Blessing of Defense"
            item.power += player.level * item_buff
        
    if themed_names[2] in player.PlayerName.lower():
        player.MHP = int(player.MHP * 15)
        player.Atk = int(player.Atk * 8)
        player.CritRate = player.CritRate / 1000

    if themed_names[3] in player.PlayerName.lower():
        player.Atk = int(player.Atk * 1.5)
        player.Def = int(player.Def * 1.5)
        player.CritDamageMod = player.CritDamageMod * ((0.005 * player.level) + 1)
        player.DodgeOdds = player.DodgeOdds / 1000

    if themed_names[4] in player.PlayerName.lower():
        player.Atk = int(player.Atk * 1.5)
        player.Def = int(player.Def * 0.5) + 1
        player.gain_crit_rate(1)
        player.CritDamageMod = player.CritDamageMod * ((0.035 * player.level) + 1)

    if themed_names[5] in player.PlayerName.lower():
        player.Vitality = player.Vitality + (0.0001 * player.level)

    if themed_names[6] in player.PlayerName.lower():
        tempname = player.PlayerName
        player.PlayerName = "Player"
        player.load()
        player.isplayer = False
        player.HOTS = []
        player.MHP = int(player.MHP / ((10000 * player.level) + 1))
        player.Atk = int(player.Atk / 5)
        player.Def = int(player.Def / 4)
        player.Regain = player.Regain / 5
        player.DodgeOdds = 0
        player.Vitality -= player.Vitality / 4

        if player.Vitality > 1:
            player.Vitality = 1

        if player.Mitigation > 1:
            player.Mitigation = 1

        player.PlayerName = tempname

    if themed_names[7] in player.PlayerName.lower():
        player.MHP = int(player.MHP * 150)

    if themed_names[8] in player.PlayerName.lower():
        player.Regain = player.Regain * (0.05 * player.level)

    if themed_names[9] in player.PlayerName.lower():
        for item in player.Items:
            item.name = "Bubbles\'s Blessing of Damage, Defense, and Utility"
            item.power += (player.level * 0.0003)


def _apply_themed_adj_modifiers(player: Player) -> None:
    if themed_ajt[0] in player.PlayerName.lower():  # atrocious
        player.MHP = int(player.MHP * 1.9)
        player.Atk = int(player.Atk * 1.1)

    if themed_ajt[1] in player.PlayerName.lower(): # baneful
        player.Atk = int(player.Atk * 1.95)
        player.CritDamageMod = player.CritDamageMod * 1.05

    if themed_ajt[2] in player.PlayerName.lower(): # barbaric
        player.MHP = int(player.MHP * 1.1)
        player.Def = int(player.Def * 1.9)

    if themed_ajt[3] in player.PlayerName.lower(): # beastly
        player.MHP = int(player.MHP * 1.05)
        player.Atk = int(player.Atk * 1.05)

    if themed_ajt[4] in player.PlayerName.lower(): # belligerent
        player.DodgeOdds = player.DodgeOdds * 1.9
        player.Atk = int(player.Atk * 1.1)

    if themed_ajt[5] in player.PlayerName.lower(): # bloodthirsty
        player.MHP = int(player.MHP - (player.MHP * 0.1))
        player.Atk = int(player.Atk + (player.Atk * 0.2))

    if themed_ajt[6] in player.PlayerName.lower(): # brutal
        player.CritRate = player.CritRate + 0.1
        player.DodgeOdds = player.DodgeOdds * 1.9

    if themed_ajt[7] in player.PlayerName.lower(): # callous
        player.Def = int(player.Def * 1.1)
        player.DodgeOdds = player.DodgeOdds * 1.9

    if themed_ajt[8] in player.PlayerName.lower(): # cannibalistic
        player.MHP = int(player.MHP + (player.MHP * 0.05))

    if themed_ajt[9] in player.PlayerName.lower(): # cowardly
        player.MHP = int(player.MHP * 1.2)
        player.Atk = int(player.Atk * 0.8)

    if themed_ajt[10] in player.PlayerName.lower(): # cruel
        player.CritDamageMod = player.CritDamageMod * 1.05

    if themed_ajt[11] in player.PlayerName.lower(): # cunning
        player.DodgeOdds = player.DodgeOdds * 1.1

    if themed_ajt[12] in player.PlayerName.lower(): # dangerous
        player.Atk = int(player.Atk * 1.05)
        player.CritRate = player.CritRate + 0.05

    if themed_ajt[13] in player.PlayerName.lower(): # demonic
        player.MHP = int(player.MHP * 1.9)
        player.Atk = int(player.Atk * 1.15)

    if themed_ajt[14] in player.PlayerName.lower(): # depraved
        player.Def = int(player.Def - (player.Def * 0.1))
        player.Atk = int(player.Atk + (player.Atk * 0.1))

    if themed_ajt[15] in player.PlayerName.lower(): # destructive
        player.Atk = int(player.Atk * 1.1)
        player.CritRate = player.CritRate + 0.05

    if themed_ajt[16] in player.PlayerName.lower(): # diabolical
        player.Atk = int(player.Atk * 1.1)
        player.DodgeOdds = player.DodgeOdds * 1.9

    if themed_ajt[17] in player.PlayerName.lower(): # disgusting
        player.Def = int(player.Def * 1.9)

    if themed_ajt[18] in player.PlayerName.lower(): # dishonorable
        player.Atk = int(player.Atk * 1.05)
        player.Def = int(player.Def * 1.95)

    if themed_ajt[19] in player.PlayerName.lower(): # dreadful
        player.Atk = int(player.Atk * 1.05)

    if themed_ajt[20] in player.PlayerName.lower(): # eerie
        player.DodgeOdds = player.DodgeOdds * 1.05

    if themed_ajt[21] in player.PlayerName.lower(): # evil
        player.MHP = int(player.MHP * 1.95)
        player.Atk = int(player.Atk * 1.05)

    if themed_ajt[22] in player.PlayerName.lower(): # execrable
        player.MHP = int(player.MHP * 1.9)

    if themed_ajt[23] in player.PlayerName.lower(): # fiendish
        player.DodgeOdds = player.DodgeOdds * 1.9
        player.CritRate = player.CritRate + 0.1

    if themed_ajt[24] in player.PlayerName.lower(): # filthy
        player.Def = int(player.Def * 1.95)

    if themed_ajt[25] in player.PlayerName.lower(): # foul
        player.Def = int(player.Def * 1.95)
        player.DodgeOdds = player.DodgeOdds * 1.95

    if themed_ajt[26] in player.PlayerName.lower(): # frightening
        player.Atk = int(player.Atk * 1.05)
        player.DodgeOdds = player.DodgeOdds * 1.95

    if themed_ajt[27] in player.PlayerName.lower(): # ghastly
        player.MHP = int(player.MHP * 1.95)
        player.DodgeOdds = player.DodgeOdds * 1.05

    if themed_ajt[28] in player.PlayerName.lower(): # ghoulish
        player.MHP = int(player.MHP * 1.95)
        player.Atk = int(player.Atk * 1.05)

    if themed_ajt[29] in player.PlayerName.lower(): # gruesome
        player.Atk = int(player.Atk * 1.05)
        player.CritDamageMod = player.CritDamageMod * 1.05

    if themed_ajt[30] in player.PlayerName.lower(): # heinous
        player.Atk = int(player.Atk * 1.1)
        player.CritDamageMod = player.CritDamageMod * 1.1

    if themed_ajt[31] in player.PlayerName.lower(): # hideous
        player.Def = int(player.Def * 1.9)
        player.MHP = int(player.MHP * 1.1)

    if themed_ajt[32] in player.PlayerName.lower(): # homicidal
        player.Atk = int(player.Atk * 1.15)

    if themed_ajt[33] in player.PlayerName.lower(): # horrible
        player.Atk = int(player.Atk * 1.02)
        player.CritRate = player.CritRate + 0.02

    if themed_ajt[34] in player.PlayerName.lower(): # hostile
        player.Atk = int(player.Atk * 1.05)
        player.Def = int(player.Def * 1.95)

    if themed_ajt[35] in player.PlayerName.lower(): # inhumane
        player.CritDamageMod = player.CritDamageMod * 1.1

    if themed_ajt[36] in player.PlayerName.lower(): # insidious
        player.Atk = int(player.Atk * 1.05)
        player.DodgeOdds = player.DodgeOdds * 1.05

    if themed_ajt[37] in player.PlayerName.lower(): # intimidating
        player.Atk = int(player.Atk * 1.95)
        player.Def = int(player.Def * 1.05)

    if themed_ajt[38] in player.PlayerName.lower(): # malevolent
        player.CritDamageMod = player.CritDamageMod * 1.05
        player.DodgeOdds = player.DodgeOdds * 1.95

    if themed_ajt[39] in player.PlayerName.lower(): # malicious
        player.Atk = int(player.Atk * 1.07)

    if themed_ajt[40] in player.PlayerName.lower(): # monstrous
        player.MHP = int(player.MHP * 1.1)
        player.Atk = int(player.Atk * 1.1)

    if themed_ajt[41] in player.PlayerName.lower(): # murderous
        player.CritRate = player.CritRate + 0.15

    if themed_ajt[42] in player.PlayerName.lower(): # nasty
        player.Atk = int(player.Atk * 1.05)
        player.Def = int(player.Def * 1.95)
        player.DodgeOdds = player.DodgeOdds * 1.95

    if themed_ajt[43] in player.PlayerName.lower(): # nefarious
        player.CritRate = player.CritRate + 0.05
        player.CritDamageMod = player.CritDamageMod * 1.05

    if themed_ajt[44] in player.PlayerName.lower(): # noxious
        player.Atk = int(player.Atk * 1.05)
        player.MHP = int(player.MHP * 1.95)

    if themed_ajt[45] in player.PlayerName.lower(): # obscene
        player.Def = int(player.Def * 1.9)
        player.DodgeOdds = player.DodgeOdds * 1.9

    if themed_ajt[46] in player.PlayerName.lower(): # odious
        player.Def = int(player.Def * 1.95)

    if themed_ajt[47] in player.PlayerName.lower(): # ominous
        player.CritRate = player.CritRate + 0.02
        player.CritDamageMod = player.CritDamageMod * 1.03

    if themed_ajt[48] in player.PlayerName.lower(): # pernicious
        player.MHP = int(player.MHP * 1.95)
        player.CritRate = player.CritRate + 0.05

    if themed_ajt[49] in player.PlayerName.lower(): # perverted
        player.Def = int(player.Def * 1.9)
        player.DodgeOdds = player.DodgeOdds * 1.1

    if themed_ajt[50] in player.PlayerName.lower(): # poisonous
        player.Atk = int(player.Atk * 1.07)
        player.MHP = int(player.MHP * 1.93)

    if themed_ajt[51] in player.PlayerName.lower(): # predatory
        player.DodgeOdds = player.DodgeOdds * 1.1
        player.CritRate = player.CritRate + 0.05

    if themed_ajt[52] in player.PlayerName.lower(): # premeditated
        player.CritRate = player.CritRate + 0.1

    if themed_ajt[53] in player.PlayerName.lower(): # primal
        player.Atk = int(player.Atk * 1.05)
        player.Def = int(player.Def * 1.95)
        player.MHP = int(player.MHP * 1.05)

    if themed_ajt[54] in player.PlayerName.lower(): # primitive
        player.Atk = int(player.Atk * 1.05)
        player.Def = int(player.Def * 1.95)

    if themed_ajt[55] in player.PlayerName.lower(): # profane
        player.MHP = int(player.MHP * 1.9)
        player.CritDamageMod = player.CritDamageMod * 1.1

    if themed_ajt[56] in player.PlayerName.lower(): # psychopathic
        player.DodgeOdds = player.DodgeOdds * 1.9
        player.Atk = int(player.Atk * 1.1)
        player.CritDamageMod = player.CritDamageMod * 1.1

    if themed_ajt[57] in player.PlayerName.lower(): # rabid
        player.Atk = int(player.Atk * 1.1)
        player.Def = int(player.Def * 1.9)

    if themed_ajt[58] in player.PlayerName.lower(): # relentless
        player.DodgeOdds = player.DodgeOdds * 1.9
        player.Atk = int(player.Atk * 1.05)
        player.CritRate = player.CritRate + 0.05

    if themed_ajt[59] in player.PlayerName.lower(): # repulsive
        player.Def = int(player.Def * 1.9)
        player.DodgeOdds = player.DodgeOdds * 1.1

    if themed_ajt[60] in player.PlayerName.lower(): # ruthless
        player.CritDamageMod = player.CritDamageMod * 1.15

    if themed_ajt[61] in player.PlayerName.lower(): # sadistic
        player.Atk = int(player.Atk * 1.02)
        player.CritDamageMod = player.CritDamageMod * 1.08

    if themed_ajt[62] in player.PlayerName.lower(): # savage
        player.Atk = int(player.Atk * 1.1)
        player.Def = int(player.Def * 1.9)
        player.MHP = int(player.MHP * 1.1)

    if themed_ajt[63] in player.PlayerName.lower(): # scary
        player.Atk = int(player.Atk * 1.95)
        player.DodgeOdds = player.DodgeOdds * 1.05
        player.CritDamageMod = player.CritDamageMod * 1.05

    if themed_ajt[64] in player.PlayerName.lower(): # sinister
        player.DodgeOdds = player.DodgeOdds * 1.05
        player.CritDamageMod = player.CritDamageMod * 1.05

    if themed_ajt[65] in player.PlayerName.lower(): # sociopathic
        player.DodgeOdds = player.DodgeOdds * 1.9
        player.Atk = int(player.Atk * 1.15)

    if themed_ajt[66] in player.PlayerName.lower(): # spiteful
        player.Atk = int(player.Atk * 1.07)
        player.MHP = int(player.MHP * 1.93)

    if themed_ajt[67] in player.PlayerName.lower(): # squalid
        player.Def = int(player.Def * 1.95)
        player.MHP = int(player.MHP * 1.05)

    if themed_ajt[68] in player.PlayerName.lower(): # terrifying
        player.Atk = int(player.Atk * 1.9)
        player.Def = int(player.Def * 1.1)

    if themed_ajt[69] in player.PlayerName.lower(): # threatening
        player.Atk = int(player.Atk * 1.05)
        player.Def = int(player.Def * 1.95)
        player.DodgeOdds = player.DodgeOdds * 1.95

    if themed_ajt[70] in player.PlayerName.lower(): # treacherous
        player.Atk = int(player.Atk * 1.05)
        player.DodgeOdds = player.DodgeOdds * 1.05
        player.CritRate = player.CritRate + 0.05

    if themed_ajt[71] in player.PlayerName.lower(): # ugly
        player.Def = int(player.Def * 1.1)
        player.MHP = int(player.MHP * 1.9)

    if themed_ajt[72] in player.PlayerName.lower(): # unholy
        player.MHP = int(player.MHP * 5)
        player.Atk = int(player.Atk * 2)
        player.CritDamageMod = player.CritDamageMod * 0.8

    if themed_ajt[73] in player.PlayerName.lower(): # venomous
        player.Atk = int(player.Atk * 1.1)
        player.MHP = int(player.MHP * 1.9)

    if themed_ajt[74] in player.PlayerName.lower(): # vicious
        player.Atk = int(player.Atk * 1.1)
        player.CritRate = player.CritRate + 0.05

    if themed_ajt[75] in player.PlayerName.lower(): # villainous
        player.Atk = int(player.Atk * 1.05)
        player.DodgeOdds = player.DodgeOdds * 1.95
        player.CritRate = player.CritRate + 0.05

    if themed_ajt[76] in player.PlayerName.lower(): # violent
        player.Atk = int(player.Atk * 1.15)
        player.Def = int(player.Def * 0.85)

    if themed_ajt[77] in player.PlayerName.lower(): # wicked
        player.Atk = int(player.Atk * 1.08)
        player.CritDamageMod = player.CritDamageMod * 1.02

    if themed_ajt[78] in player.PlayerName.lower(): # wrongful
        player.Atk = int(player.Atk * 1.05)
        player.Def = int(player.Def * 1.95)
        player.CritDamageMod = player.CritDamageMod * 1.05

    if themed_ajt[79] in player.PlayerName.lower(): # xenophobic
        player.Def = int(player.Def * 1.1)
