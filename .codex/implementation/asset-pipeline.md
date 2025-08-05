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
