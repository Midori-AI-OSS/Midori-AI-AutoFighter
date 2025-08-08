# Main Menu

Rebuilt the main menu under `aspect2d` using Panda3D DirectGUI widgets.
A top bar shows a 28×28 avatar, player name, pull count, and a banner
placeholder. The avatar is randomly chosen on first launch and persisted to
the encrypted `save.db` database. The main area displays a high‑contrast grid
of seven Lucide icon buttons. A single Run button switches between **Start**
and **Load** based on save data. Additional icons cover Edit Player, Edit
Party, Pull Characters, Options, Give Feedback, and Quit. The menu is now
instantiated by `AutoFighterApp` at startup for manual testing, with each
button exposing a stub action ready for future wiring. Selecting **Start Run**
currently launches a placeholder `RunMap` scene that displays basic routing
text.

## Testing
- `uv run pytest tests/test_menu.py::test_main_menu_structure`
