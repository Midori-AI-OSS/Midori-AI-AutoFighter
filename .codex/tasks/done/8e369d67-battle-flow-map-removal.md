# Streamline battle flow and remove map (`8e369d67`)

## Summary
Current frontend requires manual map navigation and the Run button resets ongoing runs. Battles should chain automatically without exposing the map.

## Tasks
- [ ] Fully remove the map menu; the backend should automatically pick the next room.
- [ ] After loot is collected, have the frontend load whichever room the backend returns without showing the map.
- [ ] Update the Run button so an active run resumes the current battle instead of starting over.
- [ ] Preserve run state when progressing room to room without map transitions.
- [ ] Add minimal transition feedback between rooms if needed for UX.

## Context
Feedback notes that the map slows gameplay and the Run button behavior makes testing impossible.

Status: Need Review
