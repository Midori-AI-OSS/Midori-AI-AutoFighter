# Main Menu

The main menu uses an Arknights-style grid of large [Lucide](https://lucide.dev) icons with matching text labels.

## Layout
- Arrange buttons in a 2×3 grid anchored near the bottom edge.
- Provide icons and labels for **New Run**, **Load Run**, **Edit Player**, **Options**, **Give Feedback**, and **Quit**.
- Reserve space for a centered banner above the grid and a top bar displaying the player avatar, name, and currencies.
- Place quick-access corner icons (notifications, mail, etc.) away from main content.
- Show a short tooltip on hover repeating each label for clarity.

## Give Feedback
- Include a **Give Feedback** button in the grid.
- Selecting it opens the user's browser to a pre-filled GitHub issue: `https://github.com/Midori-AI/Midori-AI-AutoFighter/issues/new?title=Feedback&body=...`.

## Navigation
- Highlight the focused icon and support keyboard or mouse selection.
- Ensure Lucide icons remain readable at large sizes across desktop and mobile resolutions.

## Background
- Fill the screen with slowly drifting, dark color clouds that subtly shift hues so icons stay legible.
