#!/usr/bin/env bash
# .agents/setup-agents.sh
# Bootstrap script for PixelArch OS (Arch-based Linux)
# Installs system dependencies and syncs frontend/backend dependencies.
# Does NOT start any servers or daemons.
#
# Tools used:
#   - yay           for system packages
#   - bun           for Node.js / frontend tooling  (never npm)
#   - uv            for Python / backend tooling     (never pip)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="${REPO_ROOT}/frontend"
BACKEND_DIR="${REPO_ROOT}/backend"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
info()  { echo "[setup] $*"; }
die()   { echo "[setup] ERROR: $*" >&2; exit 1; }

pkg_install() {
    # Install a package idempotently.
    local pkg="$1"
    yay -Syu --noconfirm --needed "$pkg"
}

# ---------------------------------------------------------------------------
# 1. System dependencies (from Dockerfile.js + Dockerfile.python)
# ---------------------------------------------------------------------------
info "Installing system dependencies..."

SYSTEM_PACKAGES=(
    curl
    wget
    git
    base-devel
    nodejs
    npm
    unzip
    bun
    uv
    docker
    docker-compose
)

for pkg in "${SYSTEM_PACKAGES[@]}"; do
    info "  -> $pkg"
    pkg_install "$pkg"
done

info "Cleaning package cache..."
yay -Yccc --noconfirm

# Ensure uv is on PATH (may be installed under ~/.local/bin)
export PATH="${HOME}/.local/bin:${PATH}"

# ---------------------------------------------------------------------------
# 2. Verify required tools are available
# ---------------------------------------------------------------------------
info "Verifying tool availability..."
command -v bun  &>/dev/null || die "bun not found on PATH after install"
command -v uv   &>/dev/null || die "uv not found on PATH after install"
command -v docker &>/dev/null || die "docker not found on PATH after install"
command -v docker-compose &>/dev/null || die "docker-compose not found on PATH after install"

info "  bun  : $(bun  --version)"
info "  uv   : $(uv   --version)"
info "  docker: $(docker --version | head -n 1)"
info "  docker-compose: $(docker-compose --version | head -n 1)"

# ---------------------------------------------------------------------------
# 3. Sync frontend dependencies (SvelteKit / Vite, using bun)
# ---------------------------------------------------------------------------
info "Syncing frontend dependencies in ${FRONTEND_DIR}..."
[[ -d "${FRONTEND_DIR}" ]] || die "frontend directory not found: ${FRONTEND_DIR}"

cd "${FRONTEND_DIR}"
info "  Installing JS dependencies with bun..."
bun install

bun run prepare || true

info "Frontend dependency sync complete."

# ---------------------------------------------------------------------------
# 4. Sync backend dependencies (Python / uv)
# ---------------------------------------------------------------------------
info "Syncing backend dependencies in ${BACKEND_DIR}..."
[[ -d "${BACKEND_DIR}" ]] || die "backend directory not found: ${BACKEND_DIR}"

cd "${BACKEND_DIR}"

info "  Removing backend uv.lock for Docker-entrypoint parity..."
rm -f uv.lock

info "  Syncing Python dependencies with uv..."
uv sync

info "Backend dependency sync complete."

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
info "Setup and dependency sync finished successfully."
info "  Backend venv    : ${BACKEND_DIR}/.venv"
