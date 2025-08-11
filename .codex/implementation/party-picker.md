# Party Picker

Builds a party selection scene with Panda3D DirectGUI that mirrors the main
menu's top bar but swaps the avatar icon for a slightly smaller home button.
The background randomly selects from `assets/textures/backgrounds` to match the
main menu. The left side hosts a vertically scrollable roster of circular
character icons, each parented to a transparent slot where a damage-type ring
overlays the portrait so the ring fully masks any corners, including the
player's avatar. The list fades at the top and bottom using dedicated gradient textures so the list
doesn't hard‑cut and omits its default frame color or horizontal scrollbar for a
clean look. Missing portraits are filled with a random
image from `assets/textures/players/fallbacks`. Each slot shows a Lucide element
icon in its corner to denote the character's damage type. Selecting an icon
overlays a green diamond image and adds the character to the party, capped at
four members.

The player's avatar is always pinned to the top of the roster and clicks route
through the same selection handler so their stats panel refreshes like any
other character. Their stats populate the panel by default so a damage type can
be chosen even on a fresh save where no other characters are owned.

Selecting any portrait swaps the 3D body preview and stat readout to match that
character. Clicking the player when their stats are uninitialized (the default
`hp=1` placeholder) returns to the Edit Player menu instead of displaying
stats, ensuring new saves guide the user through player creation before
starting a run.

A placeholder 3D body model (`body_a`, `body_b`, or `body_c`) sits in the center
and can be rotated left or right with the arrow keys. Models live in
`assets/models` as `.egg` files that are converted to `.bam` when Panda3D tools
are present; otherwise the `.egg` files load directly. The picker roots itself to
`aspect2d` so the interface is always visible. The right side displays a
tabbed stats panel grouped automatically by the `Stats` dataclass field types.
Each line includes a bullet icon that swaps to the matching element icon and
colors the text whenever a damage type name appears. A row of Lucide damage
type icons lets the player change their base element. When confirmed, the picker
launches a `RunMap` scene using the encrypted `save.db` to track consumed
seeds. A "Start Run" button in the lower-right corner triggers this transition.

Pressing the top‑left home button tears down the picker and re‑shows the
hidden `MainMenu`, ensuring the menu's right‑side command list does not overlap
the picker.

## Testing
- `uv run pytest tests/test_party_picker.py`
