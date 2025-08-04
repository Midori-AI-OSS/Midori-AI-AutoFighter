# Panda3D Migration Review

## Scope
- Evaluate effort to port Midori AI AutoFighter from Pygame to Panda3D.
- Highlight major code, asset, and architectural changes required.

## Current Stack Overview
- Core gameplay loop, rendering, input, and audio rely on Pygame.
- Assets are 2D images scaled and blitted to a single `pygame.display` surface.
- Plugins assume a procedural game loop and simple surface-based rendering.

## Migration Complexity
Porting to Panda3D would be a **major rework**. Panda3D is a full 3D engine with its own scene graph, event handling, and resource pipeline. Nearly all Pygame-specific code (rendering, input, audio, timing) would need to be rewritten using Panda3D APIs.

### Key Challenges
- **Rendering**: Replace surface blits with Panda3D scene graphs, nodes, and possibly shaders. 2D sprites may require card-based quads or conversion to 3D models.
- **Game Loop**: Pygame's loop would be replaced by Panda3D's task manager and event system, requiring refactoring of `gamestates.py` and related modules.
- **Asset Pipeline**: Current PNG/JPG assets would need packaging into Panda3D's loader format; animation and model support may need new tooling.
- **Plugins**: Player and foe plugins reference Pygame primitives; the plugin API would need redesign to interact with Panda3D objects and lifecycle.
- **Input & UI**: Pygame key events must map to Panda3D's input system. Any UI overlays would need Panda3D's DirectGUI or a custom solution.
- **Testing**: Existing test stubs mock Pygame; new abstractions or Panda3D stubs would be required for unit tests.
- **Learning Curve**: Contributors must learn Panda3D's scene graph concepts and configuration, increasing onboarding time.

### Potential Benefits
- 3D rendering pipeline and advanced lighting effects.
- Built-in resource management and window handling across platforms.
- More robust support for complex animations and future expansion.

## Effort Estimate
- **Architecture redesign**: high
- **Rendering rewrite**: high
- **Plugin API changes**: high
- **Testing and tooling**: medium
- **Total difficulty**: **High**—comparable to rewriting core gameplay.

## Recommendation
Use Panda3D only if 3D capabilities are essential. For incremental improvements to the current 2D design, extending Pygame or adopting a lighter 2D engine may be more efficient.
