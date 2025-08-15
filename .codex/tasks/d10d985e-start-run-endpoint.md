# Wire Start Run Button to Backend

## Summary
After party selection, the Start Run button should call the backend run-start endpoint and then transition the player to the floor map instead of returning to the main menu.

## Instructions
- Call `POST /run/start` with `{ "party": ["player", ...], "damage_type": "Light|Dark|Wind|Lightning|Fire|Ice" }`.
- Update the frontend so the Start Run button sends the request and handles the response.
- Store the returned `run_id` and map, then route the player to the generated map on success.

## Context
Ensures runs begin properly and the game enters map navigation.
