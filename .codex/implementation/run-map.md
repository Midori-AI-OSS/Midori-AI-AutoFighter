# Run Start and Map Display

Selecting **New Run** now opens a party picker and then a `RunMap`
scene instead of jumping straight into combat. The map uses
`MapGenerator` to build a simple floor layout with three starting paths
and renders node connections as text. Pressing **Enter** loads the first
room via `BattleRoom`, and victory automatically returns to the map
while **Esc** goes back to the main menu. The generator accepts an
optional seed store path so tests can avoid mutating the global
`used_seeds.json` file.
