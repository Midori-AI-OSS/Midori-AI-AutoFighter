# Midori AI AutoFighter - GitHub Copilot Instructions

**CRITICAL**: Always follow these instructions first and fallback to additional search and context gathering only if the information in the instructions is incomplete or found to be in error.

## Project Overview

Midori AI AutoFighter is a Python 3.12+ pygame-based arena game where fighters automatically battle endless waves of enemies. The game features a comprehensive plugin system for extending players, passives, damage-over-time effects, healing effects, and weapons.

## Essential Setup and Environment

### Install Dependencies
```bash
# Install uv package manager (REQUIRED)
pip install uv

# Verify installation
uv --version
```

### Initialize Development Environment
```bash
# Clone and enter repository
cd /path/to/Midori-AI-AutoFighter

# Install dependencies (uv creates .venv automatically)
uv sync

# Add pytest for development (if not already present)
uv add --dev pytest
```

## Core Development Commands

### Running the Application
```bash
# Start the game (requires display - will show GUI)
uv run main.py

# Note: Application requires audio/display. In headless environments, 
# expect ALSA audio errors which are normal and non-blocking.
```

### Testing
```bash
# Run all tests (52 tests, completes in ~0.7 seconds)
uv run pytest

# Run tests with verbose output
uv run pytest -v

# NEVER CANCEL: Tests complete quickly (under 1 second)
```

### Code Validation
```bash
# Compile Python files to check syntax
uv run python -m py_compile main.py

# Validate plugin templates
uv run python -m py_compile plugins/templates/*.py

# Test plugin loader functionality
uv run python -c "from plugins.plugin_loader import PluginLoader; loader = PluginLoader(); loader.discover('plugins'); print('Available players:', list(loader.get_plugins('player').keys())[:5])"
```

## Build System

### Docker-Based Distribution Build
```bash
# Navigate to builder directory
cd builder

# NEVER CANCEL: Build process takes ~1-2 minutes for Docker image
# Set timeout to 5+ minutes for safety
docker build --no-cache -t game-builder .

# NEVER CANCEL: Full build with PyInstaller takes 10-20 minutes
# Creates Windows and Linux executables
# Set timeout to 30+ minutes
bash start_build.sh

# Note: build process creates temp_game/, output/ directories
# Cleanup happens automatically after 10 minutes (sleep 600)
```

### Build Output
- `output/windows/windows_game.exe` - Windows executable
- `output/linux/linux_game` - Linux executable

## Plugin System Architecture

### Directory Structure
```
plugins/
├── players/       # Player character implementations (16+ available)
├── passives/      # Passive abilities and effects
├── dots/          # Damage-over-time effects (poison, etc.)
├── hots/          # Healing-over-time effects (regeneration, etc.)
├── weapons/       # Weapon behaviors (sword, staff, etc.)
└── templates/     # Boilerplate files for new plugins
```

### Testing Plugin System
```bash
# Verify all plugin categories load correctly
uv run python -c "
from plugins.plugin_loader import PluginLoader
loader = PluginLoader()
loader.discover('plugins')
for category in ['player', 'passive', 'dot', 'hot', 'weapon']:
    plugins = loader.get_plugins(category)
    print(f'{category}: {len(plugins)} plugins loaded')
"
```

## Critical File Locations

### Core Game Files
- `main.py` - Application entry point
- `gamestates.py` - Main game logic and state management
- `player.py` - Player character system and past lives
- `plugins/plugin_loader.py` - Dynamic plugin discovery system

### Configuration and Dependencies
- `pyproject.toml` - Project dependencies and configuration
- `.python-version` - Python 3.12 requirement
- `uv.lock` - Dependency lock file (do not edit manually)

### Documentation
- `README.md` - User-facing documentation
- `.codex/instructions/plugin-system.md` - Plugin development guide
- `.codex/implementation/` - Technical documentation
- `.codex/tasks/` - Task tracking and completed work

### Build and Deployment
- `builder/` - Docker-based build system
- `builder/dockerfile` - Multi-platform build environment
- `builder/linux/builder.sh` - Linux PyInstaller build
- `builder/windows/builder.sh` - Windows PyInstaller build (Wine-based)

## Validation Scenarios

### After Making Code Changes
1. **Always run tests first**:
   ```bash
   uv run pytest
   ```

2. **Validate the application starts**:
   ```bash
   # Should show pygame initialization and game loading
   timeout 10 uv run main.py || echo "Game started successfully"
   ```

3. **Test plugin functionality** (if plugin-related changes):
   ```bash
   uv run python -c "from plugins.plugin_loader import PluginLoader; loader = PluginLoader(); loader.discover('plugins')"
   ```

### Full End-to-End Validation
1. Run test suite: `uv run pytest`
2. Start application and verify loading: `uv run main.py`
3. Test plugin discovery: Verify all 5 plugin categories load
4. For build changes: Test Docker build process

## Common Issues and Solutions

### Environment Issues
- **"uv: command not found"**: Install uv with `pip install uv`
- **"mixer not initialized"**: Normal in headless environments, non-blocking
- **"No such file or directory (os error 2)" for pytest**: Run `uv add --dev pytest`

### Build Issues
- **Docker build fails**: Ensure Docker is running and accessible
- **PyInstaller build timeout**: NEVER CANCEL, builds can take 20+ minutes
- **Wine/Windows build issues**: Wine setup in Docker handles Windows builds

### Plugin Issues
- **Plugin not loading**: Check plugin_type attribute is set correctly
- **Import errors**: Verify plugin syntax with `python -m py_compile`

## Development Timing Expectations

- **Test suite**: ~0.7 seconds (52 tests)
- **Application startup**: ~2-3 seconds to pygame initialization
- **Docker image build**: ~1-2 minutes  
- **Full distribution build**: 10-20 minutes (NEVER CANCEL)
- **Plugin template compilation**: <0.1 seconds

## Repository Structure Summary

- **788 Python files** total in project
- **52 comprehensive tests** covering all plugin types
- **16+ player characters** available through plugin system
- **No CI workflow** currently configured (documented as needed)
- **No linting tools** configured (manual validation only)

## Working with the Codebase

### Before Making Changes
1. Read relevant documentation in `.codex/instructions/`
2. Check `.codex/tasks/` for related work and context
3. Run existing tests to establish baseline

### Making Changes
1. Keep changes minimal and focused
2. Update tests for new functionality
3. Test plugin loading if modifying plugin system
4. Validate application still starts after changes

### Code Style
- Place each import on its own line
- Sort imports by length within groups (standard library, third-party, project modules)
- Use blank lines between import groupings
- Follow existing patterns in the codebase

### Commit Guidelines
- Format: `[TYPE] Title`
- Test before committing: `uv run pytest`
- Document plugin changes in `.codex/instructions/plugin-system.md`

Remember: Always use `uv` for Python environment and dependency management. Never use `python` or `pip` directly for this project.