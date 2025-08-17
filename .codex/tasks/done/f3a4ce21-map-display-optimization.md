# Map display optimization (`f3a4ce21`)

## Summary
Map list currently reverses the full array before slicing, creating needless intermediate arrays and DOM nodes.

## Tasks
- [x] Slice the last four rooms directly from `map` and compute current room without reversing.
- [x] Update unit tests to match new logic.
- [x] Document the streamlined map rendering.

## Context
Feedback highlighted extra DOM nodes in the map component; trimming the list improves performance.
