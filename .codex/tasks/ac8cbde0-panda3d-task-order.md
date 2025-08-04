# Panda3D Remake Task Order

## Summary
Define the execution order for Panda3D remake subtasks based on the existing task list and planning document.

## Tasks
1. [ ] Project scaffold (`0f95beef`) – move legacy code, initialize uv project, install Panda3D, and set up assets and package structure.
2. [ ] Main loop and window handling (`869cac49`) – create ShowBase subclass, handle window events, and introduce scene manager skeleton.
3. [ ] Plugin loader (`56f168aa`) – build discovery system for player, foe, passive, DoT, HoT, weapon, and room plugins with event bus wrapper.
4. [ ] Damage and healing migration (`7b715405`) – port DoT/HoT logic and Stats dataclass into new architecture.
5. [ ] Main menu and settings (`0d21008f`) – implement themed menus with options for new/load runs and audio controls.
6. [ ] Player creator (`f8d277d7`) – allow body and hair customization and 100-point stat allocation with item-based extras.
7. [ ] Stat screen (`58ea00c8`) – display grouped stats, status effects, and relics with configurable refresh rate.
8. [ ] Battle room implementation (`1bfd343f`) – create combat scenes, apply stat-based accuracy, and show overtime warnings.
9. [ ] Rest room implementation (`5109746a`) – offer healing or item trades and record limited uses per floor.
10. [ ] Shop room implementation (`07c1ea52`) – sell upgrade items and cards with pricing and reroll costs.
11. [ ] Event room implementation (`cbf3a725`) – provide narrative choices with deterministic outcomes.
12. [ ] Map generation system (`3b2858e1`) – build 45-room floors, Pressure levels, and looping logic.
13. [ ] Gacha system (`4289a6e2`) – manage pulls, pity, duplicates, and reward presentation.
14. [ ] Upgrade item crafting (`418f603a`) – combine lower-star items, trade for pulls, and handle dual types.
15. [ ] SQLCipher save system (`798aafd3`) – store encrypted run data with migrations and key management.
16. [ ] Asset pipeline (`ad61da93`) – research art style, convert assets, and implement AssetManager with manifest.
17. [ ] Audio system (`7f5c8c36`) – play music and effects with volume control and boss/overtime cues.
18. [ ] UI polish and accessibility (`d6a657b0`) – apply dark glassy theme, color-blind options, and keyboard navigation.
19. [ ] Documentation and contributor guidelines (`ca46e97e`) – update README and contributor docs for new structure.
20. [ ] Testing and CI integration (`93a6a994`) – add headless tests and GitHub workflows.

## Context
Derived from the Panda3D game plan and existing Panda3D remake task list to coordinate development.

## Testing
- [ ] Run `uv run pytest`.
