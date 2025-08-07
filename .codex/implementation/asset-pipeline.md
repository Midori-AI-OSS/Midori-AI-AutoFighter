# Asset Conversion Pipeline

`tools/convert_assets.py` converts source models into Panda3D formats and
updates `assets.toml` with the generated files and SHA256 hashes. The
script caches source hashes in `tools/convert_assets.cache.json` to skip
unchanged assets.

## Requirements
- Panda3D command-line tools (`obj2egg`, `egg2bam`)
- Optional: `blend2bam` for `.blend` files (requires Blender)

## Usage
Convert a model by running:

```bash
uv run python tools/convert_assets.py <path/to/model>
```

The default output format is `.bam`. Use `--format egg` to keep `.egg`
files. Converted assets are written to `assets/models/` and recorded in
`assets.toml`.

## Example
The repository includes a sample cube model:

```bash
uv run python tools/convert_assets.py assets/src/cube.obj
```

This generates `assets/models/cube.bam` and adds an entry to
`assets.toml` with the file path and hash.

## Runtime loading

Game code retrieves assets through the `AssetManager`, which
internally uses Panda3D's global `Loader`. Some Panda3D builds expose
camelCase APIs such as `loadModel` while others provide snake_case
variants like `load_model`. The manager checks for either form when
loading models, textures, or sounds so runtime behaviour remains
portable across Panda3D releases. When loading assets manually, use
whichever style your environment provides.

The `autofighter.assets` module exposes `get_asset(category, name)`
along with convenience helpers `get_model`, `get_texture`, and
`get_audio` that call the shared `AssetManager` instance.

## Player Photos

`AssetManager.get_player_photo(name)` loads character portraits from
`assets/textures/players`. If the requested photo is missing, the manager
selects a random fallback image from
`assets/textures/players/fallbacks`. The helper is also available at the
module level via `autofighter.assets.get_player_photo`.
