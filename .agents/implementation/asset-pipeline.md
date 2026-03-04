# Asset Conversion Pipeline

`tools/convert_assets.py` converts source models into web-friendly formats (e.g., glTF) and updates `assets.toml` with the generated files and SHA256 hashes. The script caches source hashes in `tools/convert_assets.cache.json` to skip unchanged assets.

## Requirements
- Blender with glTF export or similar conversion tools

## Usage
Convert a model by running:

```bash
uv run python tools/convert_assets.py <path/to/model>
```

The default output format is `.glb`. Use `--format gltf` to keep `.gltf` files. Converted assets are written to `assets/models/` and recorded in `assets.toml`.

## Example
The repository includes a sample cube model:

```bash
uv run python tools/convert_assets.py assets/src/cube.obj
```

This generates `assets/models/cube.glb` and adds an entry to `assets.toml` with the file path and hash.

## Runtime loading

Game code retrieves assets through the `AssetManager`, which uses a generic loader for models, textures, and sounds. The manager abstracts format differences so runtime behaviour remains portable across browsers.

The `autofighter.assets` module exposes `get_asset(category, name)`
along with convenience helpers `get_model`, `get_texture`, and
`get_audio` that call the shared `AssetManager` instance.

## Player Photos

`AssetManager.get_player_photo(name)` loads character portraits from
`assets/textures/players`. If the requested photo is missing, the manager
selects a random fallback image from
`assets/textures/players/fallbacks`. The helper is also available at the
module level via `autofighter.assets.get_player_photo`.
