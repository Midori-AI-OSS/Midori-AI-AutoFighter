# Panda3D Remake Task Order

## Summary
Define the execution order for Panda3D remake subtasks based on the planning document.
Review `.codex/planning/8a7d9c1e-panda3d-game-plan.md` before starting or auditing any step.

Coders must check in with the reviewer or task master before marking tasks complete.

When working on GUI-related tasks, download and review all parts of the [Panda3D GUI manual](https://docs.panda3d.org/1.10/python/programming/gui/index). Interfaces must be built under `aspect2d`, and the downloaded documentation must not be committed to the repository.

> **Task Master Reminder:** Keep `myunderstanding.md` describing the game's flow up to date.

## Tasks
* [x] Purge legacy GUI (`purge-old-gui`) – delete existing `game/ui` modules and start a fresh UI package under `aspect2d`.
  - [x] Verify no deprecated DirectGUI code remains.
  - [x] Scaffold new menu modules following examples from the Panda3D GUI manual.
  - [x] Document the reset in `.codex/implementation`.
* [ ] Main menu rebuild (`0d21008f`) – recreate the main menu with new guidelines.
  - [ ] Implement a high-contrast grid of Lucide icons with labels.
  - [ ] Add a top bar with avatar, name, and currency counters plus a central banner.
  - [ ] Apply global DirectGUI scaling anchored to 16:9 and use themed backgrounds.
  - [ ] Stub actions for New Run, Load Run, Edit Player, Options, Give Feedback, and Quit.
  - [ ] Document this feature in `.codex/implementation` and add unit tests.
* [ ] Run start and map display (`dc3d4f2e`) – start a run when New Run is selected and show a basic floor map.
* [x] Placeholder room (`344b9c4a`) – allow entering a single unthemed room and returning to the map.
* [x] Character types (`f20caf99`) – define Type A (Masculine), Type B (Feminine), and Type C (Androgynous).
* [ ] Party picker (`f9c45e2e`) – choose four allies plus the player before beginning the run.

## Context
Derived from the Panda3D game plan. Focus on cleaning up the main menu before expanding gameplay.
