# Asset Pipeline

## Summary
Set up a pipeline for importing and optimizing art assets for Panda3D.

## Tasks
- [ ] Research low-poly or pixelated 3D art styles and evaluate free/CC model sources for compatibility.
- [ ] Establish a conversion workflow (e.g., Blender to `.bam`/`.egg`) with cached builds.
- [ ] Maintain `assets/` structure for models, textures, and audio, and create an `assets.toml` manifest mapping keys to paths and hashes.
- [ ] Build an `AssetManager` that loads and caches models, textures, and sounds on demand.
- [ ] Document guidelines for artists to contribute compatible assets.

## Context
A consistent asset pipeline ensures efficient loading and visual quality.

## Testing
- [ ] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.
