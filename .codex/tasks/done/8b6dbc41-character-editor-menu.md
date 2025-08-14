# Add character editor menu

## Summary
Create a frontend menu for editing player pronouns and damage type, calling existing backend endpoints.

## Tasks
- Implement Character Editor panel with fields for pronouns and damage type.
- Send updates to the player editor endpoint and handle validation errors.

## Context
The character editor is missing, preventing players from customizing their avatar.

## Notes
Limit pronouns to 15 characters and allow selection of Light, Dark, Wind, Lightning, Fire, or Ice.

## Outcome
An Edit button on the main menu loads the PlayerEditor overlay, pulling config from `/player/editor` and saving updates as fields change.
