# Implement crafting menu

## Summary
Provide a crafting interface to upgrade items and toggle automatic crafting.

## Tasks
- Create a Crafting button that opens the menu.
- Allow item upgrades and an auto-craft toggle.

## Context
The crafting menu is missing from the frontend.

## Notes
Match the style of other `MenuPanel` views.

## Outcome
Main menu includes a Craft button that opens `CraftingMenu`, displaying upgrade items, a manual craft action wired to `/gacha/craft`, and an auto-craft toggle hitting `/gacha/auto-craft`.
