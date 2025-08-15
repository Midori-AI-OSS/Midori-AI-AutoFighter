# Gameplay Overview

*Current status:* From a player's perspective, the Run flow is still broken. When I pick my party, the plain **Start Run** button throws me back to the main menu instead of loading the map. If I open the **Map** manually, the floor looks upside down and tapping rooms does nothing.

When I first load the web game I see a dark, glassy main menu with buttons for **Run**, **Map**, **Party**, **Edit**, **Pulls**, **Craft**, **Settings**, and **Stats**. The **Back** button kicks me to the main menu instead of the previous screen, the **Home** and **Player Editor** buttons do nothing, and the **Settings** menu lacks a voice option under audio. I can choose allies and set damage types, but actually starting a run doesn't work yet. The backend already has routes for battles, shops, and rests; the frontend just isn't talking to them from the map screen or checking for active battles.

To get the game playable, the **Start Run** and **Cancel** buttons need the stained glass style, the Start Run button must call the `/run/start` endpoint, the map should mimic Slay the Spire with the boss at the top, clicking a room should call the appropriate backend endpoint so battles or events can begin, and the UI should check if a battle is already running and lock other menus. Finished rooms should disappear so I can see my progress.

This is my current understanding of how the game behaves. I'll update it as new pieces fall into place.
