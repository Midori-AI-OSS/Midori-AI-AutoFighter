#!/usr/bin/env bash
set -euo pipefail

cd /app

# Install dependencies if node_modules missing or empty
if [[ ! -d node_modules || -z "$(ls -A node_modules 2>/dev/null || true)" ]]; then
  bun install
fi

exec bun run dev --host 0.0.0.0 --port 59001

