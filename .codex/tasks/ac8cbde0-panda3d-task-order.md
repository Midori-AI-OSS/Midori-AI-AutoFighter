# Panda3D Remake Task Order

## Summary
Define the execution order for Panda3D remake subtasks based on the existing task list and planning document.
Review `.codex/planning/8a7d9c1e-panda3d-game-plan.md` before starting or auditing any step.

Coders must check in with the reviewer or task master before marking tasks complete.

## Tasks
1. [x] Project scaffold (`0f95beef`) – move legacy code, initialize uv project, install Panda3D, and set up assets and package structure.
2. [x] Main loop and window handling (`869cac49`) – create ShowBase subclass and handle window events.
3. [x] Scene manager (`dfe9d29f`) – swap menus, gameplay scenes, and overlays.
4. [x] Plugin loader (`56f168aa`) – discover player, foe, passive, DoT, HoT, weapon, and room plugins.
5. [x] Event bus wrapper (`120c282f`) – expose decoupled messaging so plugins can emit and subscribe.
6. [x] Stats dataclass (`751e73eb`) – share core attributes between players and foes.
7. [x] Damage and healing migration (`7b715405`) – port DoT/HoT logic into new architecture.
8. [x] Main menu (`0d21008f`) – themed entry screen with New Run, Load Run, Edit Player, Options, and Quit.
9. [x] Options submenu (`8e57e5f2`) – sound-effects volume, music volume, and stat-screen pause toggle.
10. [x] Player customization (`f8d277d7`) – body types, hair styles, colors, and accessories.
11. [x] Stat allocation (`4edfa4f8`) – 100‑point pool granting +1% increments per stat.
12. [x] Item bonus confirmation (`c0fd96e6`) – ensure upgrade-item points persist after player creation.
13. [x] Stat screen display (`58ea00c8`) – grouped stats, status effects, and relics.
14. [x] Stat screen refresh control (`5855e3fe`) – configurable update frequency.
15. [x] Battle room core (`1bfd343f`) – combat scenes with stat-driven accuracy.
16. [x] Overtime warnings (`4e282a5d`) – flash room after 100 turns or 500 on floor bosses.
17. [x] Rest room features (`5109746a`) – healing or item trades with per-floor limits.
18. [x] Shop room features (`07c1ea52`) – sell upgrade items and cards with reroll costs.
19. [x] Event room narrative (`cbf3a725`) – deterministic choice outcomes.
20. [x] Map generator (`3b2858e1`) – 45-room floors and looping logic.
21. [x] Pressure level scaling (`6600e0fd`) – adjust foe stats, room counts, and extra bosses.
22. [x] Boss room encounters (`21f544d8`) – implement standard boss fights.
23. [x] Floor boss escalation (`51a2c5da`) – handle difficulty spikes and rewards each loop.
24. [x] Chat room interactions (`4185988d`) – one-message LLM chats after battles.
25. [x] Reward tables (`60af2878`) – define drops for normal, boss, and floor boss fights.
26. [x] Gacha pulls (`4289a6e2`) – spend upgrade items on character rolls.
27. [x] Gacha pity system (`f3df3de8`) – raise odds until a featured character drops.
28. [ ] Duplicate handling (`6e2558e7`) – apply stack rules and Vitality bonuses.
28. [x] Duplicate handling (`6e2558e7`) – apply stack rules and Vitality bonuses.
29. [x] Gacha presentation (`a0f85dbd`) – play rarity video and show results menu.
30. [ ] Upgrade item crafting (`418f603a`) – combine lower-star items into higher ranks.
31. [ ] Item trade for pulls (`38fe381f`) – exchange 4★ items for gacha tickets.
32. [x] SQLCipher schema (`798aafd3`) – store run and player data securely.
33. [x] Save key management (`428e9823`) – derive and back up salted-password keys.
34. [ ] Migration tooling (`72fc9ac3`) – versioned scripts for forward-compatible saves.
35. [ ] Asset style research (`ad61da93`) – choose art direction and free model sources.
36. [x] Conversion workflow (`10bd22da`) – build pipeline to Panda3D formats.
37. [ ] AssetManager with manifest (`d5824730`) – load and cache assets via `assets.toml`.
38. [x] Audio system (`7f5c8c36`) – play music and effects with volume control.
39. [ ] UI polish and accessibility (`d6a657b0`) – dark glass theme, color-blind mode, keyboard navigation.
40. [ ] Documentation and contributor guidelines (`ca46e97e`) – update README and contributor docs for new structure.
41. [ ] Testing and CI integration (`93a6a994`) – add headless tests, GitHub workflows, and run `uv run pytest` last.

## Context
Derived from the Panda3D game plan and existing Panda3D remake task list to coordinate development.
