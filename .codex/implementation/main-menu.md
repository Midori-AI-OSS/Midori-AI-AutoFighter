# Main Menu

Implemented in `game/ui/menu.py`, the main menu presents an Arknights-inspired grid of Lucide icons anchored near the bottom of the screen. Buttons provide access to **New Run**, **Load Run**, **Edit Player**, **Options**, **Give Feedback**, and **Quit**. Starting a new run opens a party picker before the map.

The top bar now displays the player's portrait alongside basic currency info, and a central banner uses themed artwork. Additional corner icons reserve space for notifications and quick actions. A static dark backdrop keeps the interface readable without distracting animation.

Top-left quick-access buttons for **Home**, **Pulls**, and **Crafting** are anchored flush against the corner without the word "button" in their labels. Text throughout the menu now scales using the global widget scale so it remains readable on all displays, and a placeholder frame sits in the bottom-left quadrant for the eventual player model preview.

Selecting **Give Feedback** attempts to open a pre-filled GitHub issue in the user's browser. If this fails, an in-game label displays the URL so it can be entered manually during play or accessed by tests.

The menu supports keyboard and mouse navigation through DirectGUI widgets and delegates option adjustments to `OptionsMenu`.
