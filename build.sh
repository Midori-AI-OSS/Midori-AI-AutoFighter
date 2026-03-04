#!/bin/bash

# Build script for Midori AutoFighter
# Usage: ./build.sh [platform]
# Platforms: linux, darwin (macOS) - auto-detected if not specified

set -e

PLATFORM=${1:-$(uname -s | tr '[:upper:]' '[:lower:]')}

echo "Building Midori AutoFighter - Platform: $PLATFORM"

# Desktop builds (Linux/macOS) - build backend + frontend
echo "Building desktop application..."

# Build frontend first
echo "Building frontend..."
cd frontend

# Detect available Node tools
if command -v bun >/dev/null 2>&1; then
  echo "Using bun for Node.js environment"
  bun install
  bun run build
else
  echo "bun not found, using npm"
  npm install
  npm run build
fi

cd ..

# Build backend
echo "Setting up backend build environment..."
cd backend

# Setup environment with tool detection
if command -v uv >/dev/null 2>&1; then
  echo "Using uv for Python environment"
  echo "Installing backend dependencies..."
  uv sync
  
  # Install PyInstaller
  echo "Installing PyInstaller..."
  uv add --dev pyinstaller
  
  # Build executable
  echo "Building executable..."
  PYTHON_RUN="uv run"
else
  echo "uv not found, using standard Python tools"
  
  if [ ! -d "venv" ]; then
    python3 -m venv venv
  fi
  source venv/bin/activate
  
  echo "Installing backend dependencies..."
  pip3 install -e .
  
  # Install PyInstaller
  echo "Installing PyInstaller..."
  pip3 install pyinstaller
  
  # Build executable
  echo "Building executable..."
  PYTHON_RUN="python3 -m"
fi

DATA_ARGS="--add-data ../frontend/build:frontend"

OUTPUT_NAME="stained-glass-odyssey-endless-standard-$PLATFORM"

echo "Building: $OUTPUT_NAME"
$PYTHON_RUN pyinstaller --onefile $DATA_ARGS --clean --name "$OUTPUT_NAME" app.py

echo "Build completed successfully!"
echo "Output: dist/$OUTPUT_NAME"
echo "Size: $(du -h dist/$OUTPUT_NAME | cut -f1)"
