# Main Menu

Implemented in `game/ui/menu.py`, the main menu presents an Arknights-inspired grid of Lucide icons anchored near the bottom of the screen. Buttons provide access to **New Run**, **Load Run**, **Edit Player**, **Options**, **Give Feedback**, and **Quit**. Starting a new run opens a party picker before the map.

A top bar shows placeholder player information and a central banner, while additional corner icons reserve space for notifications and other quick actions. A dark, slowly shifting cloud backdrop keeps the interface readable.

Selecting **Give Feedback** attempts to open a pre-filled GitHub issue in the user's browser. If this fails, an in-game label displays the URL so it can be entered manually during play or accessed by tests.

The menu supports keyboard and mouse navigation through DirectGUI widgets and delegates option adjustments to `OptionsMenu`.
