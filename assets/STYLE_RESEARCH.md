# Asset Style Research

## Style Overview

### Low-Poly
- Uses relatively few polygons, giving it a simple, angular look that suits real-time applications and retro aesthetics.
- Planning calls for a look reminiscent of *Final Fantasy VII* and *VIII* to keep assets lightweight.
- Converts well from formats like `.blend` or `.fbx` into Panda3D's `.bam`/`.egg` with Blender export tools.

### Pixelated 3D
- Combines pixel-art textures or voxel geometry with 3D models to preserve chunky pixels.
- Works by disabling texture filtering or by building models from voxel "pixels" for a retro hybrid style.
- Shares tooling with low-poly pipelines but benefits from nearest-neighbor texture settings.

## Free or CC Model Sources
| Source | License | Common Formats | Notes |
|-------|---------|----------------|-------|
| [Poly Haven](https://polyhaven.com/) | CC0 | `.blend`, `.gltf`, `.fbx` | High-quality environment and prop models, plus textures.
| [Quaternius](https://quaternius.com/) | CC0 | `.blend`, `.fbx`, `.obj`, `.dae`, `.gltf` | Large low-poly model packs ideal for prototyping.
| [Kenney](https://kenney.nl/assets) | CC0 | `.blend`, `.glb`, `.fbx`, `.obj` | Extensive themed packs with consistent art direction.
| [OpenGameArt](https://opengameart.org/) | Varies (CC0, CC-BY, GPL) | `.blend`, `.fbx`, `.obj`, and more | Community-contributed assets; verify license per download.

### Notes
- Panda3D loads models most efficiently in `.bam` but accepts `.egg`. Convert source files during build steps.
- Keep textures power-of-two sized; pixelated styles should use nearest-neighbor filtering to avoid blurring.
- For voxel or pixel hybrids, consider tools like MagicaVoxel or Blender's pixel-art shaders.

## References
- Panda3D planning doc lines 167-170 on art style and conversion workflow.
- Wikipedia summaries of low poly, pixel art, and voxel art for definitions.
- Source sites above for license and format availability.
