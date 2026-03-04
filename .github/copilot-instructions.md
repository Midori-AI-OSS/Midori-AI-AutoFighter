# Stained Glass Odyssey: Endless Development Instructions

**ALWAYS follow these instructions first**. Only search for additional information or run exploration commands if the information here is incomplete or contradicted by actual behavior.

<!-- MCP TOOLS REMINDER -->
> NOTE FOR CODING AGENTS: Use MCP-style helper tools for task planning and research. Always prefer the `sequentialthinking` (sequential thought planning) tool for multi-step reasoning and the Context7 tools (e.g., `mcp_context7_resolve-library-id` / `mcp_context7_get-library-docs`) when you need up-to-date library documentation or API references. These tools improve traceability and should be used for all non-trivial tasks.


## Repository Overview

Stained Glass Odyssey: Endless is a web-based auto-battler game with a Svelte frontend and Python Quart backend. The repository supports local builds for Linux and macOS.

### Directory Structure
- `backend/` - Python Quart backend with game logic and services
- `frontend/` - Svelte frontend with responsive design  
- `legacy/` - Previous Pygame version (read-only, do not modify)
- `.agents/` - Documentation and contributor guides

## Required Tools Installation

Tools are now autoinstalled into your dev env.

**CRITICAL**: Always use `uv` for Python and `bun` for Node.js. Never use `pip` or `npm` directly as they are slower and not compatible with the repository's tooling.

## Development Workflow

### 1. Bootstrap and Test the Repository

**MANDATORY**: Always run the full test suite first to understand the current state:

```bash
# Run all tests - takes ~2 minutes. NEVER CANCEL.
./run-tests.sh
```

**Timeout Warning**: Set timeout to 180+ seconds. Some backend tests may take up to 15 seconds each, and the full suite runs ~60+ tests.

**Expected Result**: Most tests should pass. Some tests may fail (this is normal for active development). One test (`backend tests/test_app.py`) typically times out at 15 seconds - this is expected.

### 2. Building the Application

#### Quick Build
```bash
# Build standard profile - takes ~1 minute. NEVER CANCEL.
./build.sh

# Build for specific platform
./build.sh linux
```

**Timeout Warning**: Set timeout to 120+ seconds for builds.

**Expected Output**: 
- Standard build: executable in `backend/dist/stained-glass-odyssey-endless-standard-<platform>`
- Build artifacts also created in `backend/build/` directory

### 3. Running the Application

#### Backend Only
```bash
cd backend
uv run app.py
```

**Expected**: Server starts on `http://localhost:59002`.

#### Frontend Development
```bash
cd frontend
bun run dev
```

**Expected**: Development server starts on `http://localhost:59001`

#### Frontend Build
```bash
cd frontend
bun run build
```

**Timeout**: Takes ~18 seconds. Set timeout to 60+ seconds.

#### Docker Compose (LIMITATION)
```bash
# KNOWN ISSUE: Currently fails due to network connectivity problems
docker compose up --build frontend backend
```

**Status**: Docker builds currently fail due to DNS resolution issues in the build environment. Use direct backend/frontend execution instead.

## Linting and Code Quality

### Backend Linting (MANDATORY)
```bash
# ALWAYS run before committing
uv tool run ruff check backend --fix

# Check entire repository  
uv tool run ruff check . --fix
```

**Expected Result**: Should show "All checks passed!" when no issues remain, or "Found X errors (X fixed, 0 remaining)" when fixes are applied.

### Frontend Linting
```bash
cd frontend
bun run lint        # Check for issues
bun run lint:fix    # Auto-fix issues
```

**Known Issues**: Some linting errors currently exist in the frontend. These do not block development but should be addressed.

## Testing

### Running Individual Tests
```bash
# Backend tests
cd backend
uv run pytest tests/test_specific_file.py

# Frontend tests  
cd frontend
bun test tests/specific.test.js
```

### Test Timeouts
- **Local Development**: Tests auto-cancel after 15 seconds
- **CI Environment**: No timeout limits
- **Full Test Suite**: Takes ~2 minutes total

## Validation Scenarios

After making changes, ALWAYS test these scenarios:

### 1. Basic Backend API Test
```bash
# Start backend
cd backend && uv run app.py

# In another terminal, test API
curl http://localhost:59002/
# Expected: {"flavor":"default","status":"ok"}
```

### 2. Build Validation
```bash
# Test standard Linux build works
./build.sh linux
ls -la backend/dist/stained-glass-odyssey-endless-standard-linux
# Expected: ~549MB executable file
```

### 3. Frontend Build Validation
```bash
cd frontend
bun run build
ls -la build/
# Expected: Generated static files including _app/ directory and effekseer.wasm (~1.1MB)
```

## Build Variants and Platforms

### Available Variants
- **standard**: base profile

### Supported Platforms
- **Linux**: supported
- **macOS**: supported

## Known Issues and Limitations

### 1. Executable Plugin Discovery
Built executables may fail with plugin discovery errors. This is a known issue in the build process.

### 2. Docker Compose Networking
Docker builds currently fail due to DNS resolution problems. Use direct execution instead.

### 3. Test Failures
Some tests may fail in active development. Only fix test failures related to your specific changes.

## CI/CD Integration

### GitHub Actions
- **Build workflows**: Automatically build on push/PR
- **Test workflows**: Run complete test suite
- **Linting**: Separate jobs for backend (`uvx ruff check`) and frontend (`bunx eslint`)

### Required Checks
Before pushing changes:
```bash
# 1. Run linting
uv tool run ruff check backend --fix
cd frontend && bun run lint:fix

# 2. Run tests
./run-tests.sh

# 3. Test builds (optional for minor changes)
./build.sh non-llm
```

## Project Structure Navigation

### Key Backend Files
- `backend/app.py` - Main application entry point
- `backend/game.py` - Core game logic
- `backend/autofighter/` - Game mechanics
- `backend/plugins/` - Character and ability plugins
- `backend/routes/` - API endpoints

### Key Frontend Files  
- `frontend/src/` - Svelte components
- `frontend/static/` - Static assets
- `frontend/build/` - Built output (generated)

### Configuration Files
- `backend/pyproject.toml` - Python dependencies
- `frontend/package.json` - Node.js dependencies
- `ruff.toml` - Python linting configuration
- `compose.yaml` - Docker configuration

## Emergency Procedures

### Build Stuck or Failed
1. Check if process is still running with `ps aux | grep python`
2. If stuck, kill with `pkill -f pyinstaller`
3. Clean build artifacts: `rm -rf backend/build backend/dist`
4. Retry build

### Test Failures
1. Run individual failing test: `cd backend && uv run pytest tests/test_file.py -v`
2. Check if failure is related to your changes
3. If unrelated, document and proceed

### Development Environment Issues
2. Clear caches: `uv cache clean`
3. Restart development servers

Remember: Follow the AGENTS.md contributor guidelines and use the appropriate contributor mode documentation in `.agents/modes/` for your role.
