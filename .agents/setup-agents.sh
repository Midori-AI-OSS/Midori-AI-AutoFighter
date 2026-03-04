#!/usr/bin/env bash
# .agents/setup-agents.sh
# Bootstrap script for PixelArch OS (Arch-based Linux)
# Installs all system dependencies and builds both frontend (JS) and backend (Python).
# Does NOT start any servers or daemons — build only.
#
# Tools used:
#   - yay / pacman  for system packages
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
    # Prefers yay when available (handles AUR + official); falls back to pacman.
    local pkg="$1"
    if command -v yay &>/dev/null; then
        yay -S --noconfirm --needed "$pkg"
    else
        sudo pacman -S --noconfirm --needed "$pkg"
    fi
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
)

for pkg in "${SYSTEM_PACKAGES[@]}"; do
    info "  -> $pkg"
    pkg_install "$pkg"
done

# Ensure uv is on PATH (may be installed under ~/.local/bin)
export PATH="${HOME}/.local/bin:${PATH}"

# ---------------------------------------------------------------------------
# 2. Verify required tools are available
# ---------------------------------------------------------------------------
info "Verifying tool availability..."
command -v bun  &>/dev/null || die "bun not found on PATH after install"
command -v uv   &>/dev/null || die "uv not found on PATH after install"

info "  bun  : $(bun  --version)"
info "  uv   : $(uv   --version)"

# ---------------------------------------------------------------------------
# 3. Build frontend (SvelteKit / Vite, using bun)
# ---------------------------------------------------------------------------
info "Building frontend in ${FRONTEND_DIR}..."
[[ -d "${FRONTEND_DIR}" ]] || die "frontend directory not found: ${FRONTEND_DIR}"

cd "${FRONTEND_DIR}"
info "  Installing JS dependencies with bun..."
bun install --frozen-lockfile

info "  Running bun run build..."
bun run build

info "Frontend build complete."

# ---------------------------------------------------------------------------
# 4. Build backend (Python / uv)
# ---------------------------------------------------------------------------
info "Building backend in ${BACKEND_DIR}..."
[[ -d "${BACKEND_DIR}" ]] || die "backend directory not found: ${BACKEND_DIR}"

cd "${BACKEND_DIR}"

info "  Creating / syncing Python virtual environment with uv..."
# uv sync creates the venv if it does not exist and installs all deps.
# --python ensures we use Python 3.13 consistent with the Dockerfile.
uv sync --python python3.13

info "  Compiling Python bytecode..."
uv run python -m compileall -q .

info "Backend build complete."

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
info "All builds finished successfully."
info "  Frontend output : ${FRONTEND_DIR}/.svelte-kit/ (or build/)"
info "  Backend venv    : ${BACKEND_DIR}/.venv"
