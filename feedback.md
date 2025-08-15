## Layout and key elements of the combat UI

Action Order bar (left-top side) – A vertical timeline shows portraits of enemies and allies in the order they will act.  Characters move down the bar as time advances; icons can appear multiple times if passive or Ultimate abilities cause extra turns.  You can monitor upcoming turns to plan when to use skills or defensive actions.

Enemy status (top‑centre) – Each enemy has a health bar (red gauge) with a toughness shield underneath and weakness icons underneath the shield.  When the toughness bar is depleted with the correct element, the enemy enters a “Break” state that delays its next turn and applies an element‑specific debuff.  Bosses may have dots above the health bar to show phase counters – each dot disappears when a health threshold is crossed.  Selecting an enemy displays a crosshair around it and shows its level and type on the top right.

Top‑right controls (Speed and Pause) – Buttons in the upper right let you toggle 2× speed to accelerate animations or pause to open the settings menu.  These controls are often annotated in guides as “two right‑pointing arrows” (speed), the pause symbol.

Special mechanics indicators – When certain passive or Ultimate effects trigger, the timeline highlights extra turns or priority jumps.  For example, the Ultimate Queue Jump shows a golden frame pushing a character’s icon up the timeline, while passive abilities like “Girl Power” highlight multiple icons to denote an upcoming extra action.  Counters or follow‑up attacks also insert new icons on the timeline.

Enemy information panels – Clicking the small “i” icon under an enemy’s toughness bar opens a side panel with tabs for description and skills; this lets you read their abilities and check weaknesses before committing your actions.

The same guide illustrates Ultimate energy costs by pointing arrows at the Energy meters beneath each character; once full, a bright glow signals that the Ultimate can be activated.

Double‑speed function are enabled through the top‑right buttons.  A demonstration screenshot shows the controls while characters fight automatically in the background.


## Frontend issues
The settings panel is now completely incorrect. It does not offer three different columns. Column 1 should be audio, column 2 should be system or gameplay, and column 3 should be all other settings. There's no framerate setting that should be locked to 30, 60, 120 frames, and that will control the polling rate of the server. There's no way to set the autocraft setting in the settings menu, and it does not follow the standard of using the game view point.

The menu that was supposed to be on the right-hand side somehow got removed, and now is only showing the combat. We need to remove the Shortcuts menu and move everything that's in the Shortcuts menu, remove the text, and put it back on the stained-glass, dark-themed right sidebar on the side.

On desktop, drop the party viewer and target stat windows and expand the game viewport to roughly 95% of the screen while keeping the current menu behavior.
