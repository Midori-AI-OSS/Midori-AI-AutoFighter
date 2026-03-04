# Codex LRM Backend Foundation Plan

## Scope

This plan defines a phased migration path from legacy LRM references toward a Codex CLI-backed LRM foundation.

## Phase 0 (Planning and Documentation)

### Goals
- Capture a decision-complete implementation spec for Codex CLI-based LRM integration.
- Remove stale references that imply the old framework-based LRM path is still active.
- Keep scope explicit and phased so backend foundation changes remain controlled.

### Non-goals
- No gameplay integration changes in this phase.
- No map-generation chat-room expansion in this phase.
- No frontend LRM tab reintroduction in this phase.

### Current state snapshot
- Chat rooms currently return empty responses while LRM integration is disabled.
- `/config/lrm` runtime endpoints are part of the backend foundation scope.
- Multiple docs/config templates still mention legacy framework wiring and old LangChain-based flows.

### Deliverable
- This file serves as the implementation handoff specification.

## Phase 1 (Backend Foundation)

### Summary
Add backend-only Codex LRM foundation components with safe defaults, explicit opt-in, and no map/frontend expansion.

### Runtime design
- Provider model:
  - `disabled` (default)
  - `codex_cli`
- Configuration persistence:
  - Store selected provider/model/reasoning/summary in `options` table.
- Safety defaults:
  - Provider defaults to `disabled`.
  - Failures should degrade to empty chat responses without breaking run flow.

### Backend interfaces
- `GET /config/lrm`
  - Returns current config, defaults, and provider list.
- `POST /config/lrm`
  - Validates and persists config updates.
- `POST /config/lrm/test`
  - Executes a one-shot probe prompt through Codex CLI for diagnostics.

### Internal service API
- Add `backend/services/lrm_service.py` with:
  - Config normalization/validation helpers.
  - Option-store read/write wrappers.
  - Codex CLI execution wrapper with timeout handling.
  - Chat prompt helper used by chat-room runtime path.

### Chat room behavior
- Keep payload shape stable (`response`, `voice`, etc.).
- When provider is `codex_cli`, attempt one-shot response generation.
- On any error/missing binary/timeout, return empty response and continue run safely.

### Error handling
- Validate provider/model/reasoning/summary values before persistence.
- Return structured diagnostic fields from `/config/lrm/test`.
- Avoid raising uncaught errors on subprocess failures.

### Observability
- Include duration/exit-code diagnostics in test endpoint responses.
- Keep logs free of secrets and prompt dumps unless explicitly needed for debug mode.

## Phase 2 (Doc + Config Cleanup)

### Active docs/config files to align
- `.agents/implementation/agent-config.md`
- `.agents/implementation/event-room.md`
- `.agents/implementation/game-workflow.md`
- `.agents/implementation/map-generator.md`
- `.agents/implementation/player-foe-reference.md`
- `.agents/implementation/settings-menu.md`
- `backend/.agents/implementation/lrm-config.md`
- `backend/.agents/implementation/llm-loader.md`
- `backend/.agents/implementation/memory-backend.md`
- `frontend/.agents/implementation/lrm-settings.md`
- `frontend/.agents/implementation/settings-menu.md`
- `frontend/.agents/implementation/backend-discovery.md`
- `backend/config.toml`
- `backend/config.toml.example`

### Rewrite rules
- Remove statements claiming active legacy framework wiring.
- Mark old LangChain/loader references as retired where applicable.
- Describe Codex-based LRM support as active only where runtime now supports it.
- Keep terminology aligned with repository preference: `LRM`.

## Test Plan

### Backend verification
- Add/update tests for:
  - `GET /config/lrm` defaults and structure.
  - `POST /config/lrm` validation and persistence.
  - `POST /config/lrm/test` success/failure behavior with mocked subprocess.
  - Non-LRM endpoints still functioning when LRM provider is disabled.

### Regression checks
- Chat room resolve path remains non-fatal when Codex execution fails.
- Existing gameplay flow remains unchanged when provider is disabled.

## Risks and Mitigations

### Risk: Codex binary unavailable in runtime environment
- Mitigation: detect missing binary and return controlled error from test endpoint; chat path degrades gracefully.

### Risk: Timeout/stuck subprocess
- Mitigation: bounded timeout with kill-and-collect cleanup.

### Risk: stale docs causing implementation confusion
- Mitigation: complete cleanup pass in active implementation docs and templates in same delivery stream.

## Acceptance Criteria
- Planning file exists and is committed.
- Backend foundation routes/service implemented with disabled-by-default behavior.
- Chat runtime path uses Codex provider only when enabled and remains safe on failure.
- Stale legacy LRM references are removed or explicitly marked retired in active implementation docs.
- Targeted backend tests pass for new/updated behaviors.
