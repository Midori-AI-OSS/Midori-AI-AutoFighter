# Hook run button to floor map

## Summary
Replace the Run placeholder with a party picker and map view so starting a run displays the generated floor.

## Tasks
- Show a party picker modal when Run is clicked.
- After confirmation, load and render the floor map instead of placeholder text.

## Context
Players cannot begin runs because the Run button does not open the map.

## Notes
Use the existing `MapDisplay` component for the map view.

## Outcome
Run button opens a party picker modal and, on confirmation, displays the generated floor map.
