#!/usr/bin/env bash
set -euo pipefail

# Ensure we are in the mounted app directory
cd /app

# Default DB lives under /app/save.db; override via AF_DB_PATH if needed
export PYTHONPATH="/app:${PYTHONPATH:-}"

rm -f uv.lock

echo installing backend dependencies
uv sync
exec uv run app.py


