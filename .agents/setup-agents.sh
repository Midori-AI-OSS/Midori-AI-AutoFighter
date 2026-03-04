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

REPO_ROOT="$(pwd)"
FRONTEND_DIR="${REPO_ROOT}/frontend"
BACKEND_DIR="${REPO_ROOT}/backend"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
info()  { echo "[setup] $*"; }
die()   { echo "[setup] ERROR: $*" >&2; exit 1; }

[[ -f "${REPO_ROOT}/AGENTS.md" ]] || die "run this script from the repository root"

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

info "  Syncing Python dependencies with uv..."
uv sync

info "Backend dependency sync complete."

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
info "Setup and dependency sync finished successfully."
info "  Backend venv    : ${BACKEND_DIR}/.venv"
