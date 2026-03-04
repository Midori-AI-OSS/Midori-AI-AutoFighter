# LRM Provider Runtime

The legacy LangChain loader path is retired. Runtime LRM execution now uses the
Codex CLI provider flow implemented in `backend/services/lrm_service.py`.

## Provider Modes

- `disabled` (default): no external LRM execution.
- `codex_cli`: one-shot Codex CLI calls for configured operations.

## Configuration

Runtime settings are stored in `options` and managed via `/config/lrm`:

- `lrm_provider`
- `lrm_model`
- `lrm_reasoning_effort`
- `lrm_summary`

## Execution Model

- Provider calls are asynchronous subprocess executions.
- Timeouts are enforced (`AF_LRM_TIMEOUT_SECONDS`, default `20`).
- Missing binary, timeout, or non-zero exits return controlled errors.
- Gameplay-facing chat paths degrade safely to empty responses on failures.
