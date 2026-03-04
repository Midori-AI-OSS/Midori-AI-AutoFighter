# Midori AutoFighter Build System

This document describes how to build the Midori AutoFighter game locally for supported platforms.

### Platforms
- **Linux** (x64)
- **macOS** (x64/ARM64)

## Local Development

### Prerequisites
- [uv](https://github.com/astral-sh/uv) for Python dependency management
- [bun](https://bun.sh/) for frontend tooling
- Python 3.12+

### Quick Build
Use the provided build script:

```bash
# Build for current platform
./build.sh

# Build for specific platform
./build.sh linux
```

### Manual Build Process

1. **Setup environment:**
   ```bash
   cd backend
   uv sync
   ```

2. **Build frontend assets:**
   ```bash
   cd ../frontend
   bun install
   bun run build
   ```

3. **Install PyInstaller:**
   ```bash
   cd ../backend
   uv add --dev pyinstaller
   ```

4. **Build executable:**
   ```bash
   uv run pyinstaller --onefile --add-data ../frontend/build:frontend --clean --name stained-glass-odyssey-endless-standard app.py
   ```

## Troubleshooting

### Common Issues

1. **Missing Tooling**: Install `uv` and `bun` first.
2. **Frontend Build Errors**: Run `bun install` before `bun run build`.

### Build Optimization

To reduce build size:
- Use `--onefile` flag (already included)
- Consider excluding unused dependencies with `--exclude-module`

## Contributing

When adding new dependencies:
1. Add base dependencies to the main `dependencies` list in `pyproject.toml`
2. Keep `build.sh` aligned with the current dependency model
3. Test builds locally before pushing

## Architecture

```
backend/                    # Backend game logic
├── app.py                  # Application entry point
├── pyproject.toml          # Dependencies and build config
└── [game source files]

frontend/                   # Frontend UI
├── src/                    # Svelte components
└── package.json            # Node dependencies

build.sh                    # Local build helper script
```
