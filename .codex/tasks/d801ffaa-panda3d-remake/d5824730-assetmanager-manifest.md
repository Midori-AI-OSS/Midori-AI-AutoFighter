# AssetManager with Manifest

## Summary
Implement an AssetManager that loads resources via an `assets.toml` manifest.

## Tasks
- [ ] Create an `assets.toml` mapping logical keys to file paths and hashes.
- [ ] Build an AssetManager to load and cache models, textures, and sounds.
- [ ] Expose a simple API for other systems to request assets by key.
- [ ] Document this feature in `.codex/implementation`.
- [ ] Add unit tests covering success and failure cases.

## Context
A manifest-driven manager centralizes asset loading and eases caching.

## Testing
- [ ] Run `uv run pytest`.

Once complete, update this task with `status: ready for review` and request an auditor to update this status.
status: in progress
