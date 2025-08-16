# Add Docker Compose Profiles for LLM Extras

## Summary
Expose optional LLM extras through Docker Compose profiles so developers can run GPU- or CPU-accelerated models alongside the game.

## Tasks
- Define `llm-cuda`, `llm-amd`, and `llm-cpu` profiles in `compose.yaml`.
- Document how to launch these profiles in `README.md`.

## Acceptance Criteria
- `compose.yaml` includes separate profiles for each LLM extra.
- README explains how to start profiles with `docker compose --profile`.
