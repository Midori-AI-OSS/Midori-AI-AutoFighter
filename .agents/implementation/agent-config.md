# Agent Configuration

## Status

The legacy framework-based LRM config path has been retired.

Current runtime LRM settings are stored in the backend `options` table and are managed through the `/config/lrm` endpoints.

## Runtime Configuration Source

- `GET /config/lrm` returns the effective provider/model/reasoning settings.
- `POST /config/lrm` validates and persists configuration updates.
- `POST /config/lrm/test` runs a one-shot Codex CLI probe for diagnostics.

## Provider Model

- `disabled` (default): chat rooms return empty responses.
- `codex_cli`: chat rooms attempt one-shot Codex-generated replies.

## Legacy Templates

`backend/config.toml` and `backend/config.toml.example` are reference templates only and are not auto-loaded by runtime.
