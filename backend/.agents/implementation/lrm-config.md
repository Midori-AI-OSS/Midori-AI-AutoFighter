# LRM Configuration

Backend LRM configuration is managed through runtime endpoints backed by persisted `options` values.

## Endpoints

- `GET /config/lrm`
  - Returns provider status, model, reasoning settings, defaults, and provider list.
- `POST /config/lrm`
  - Validates and persists provider/model/reasoning/summary settings.
- `POST /config/lrm/test`
  - Runs a one-shot prompt through Codex CLI and returns structured diagnostics.

## Chat Room Integration

`ChatRoom.resolve()` reads effective LRM settings and:

- Calls Codex CLI when provider is `codex_cli`.
- Returns empty response when provider is `disabled` or execution fails.

This behavior keeps room payload shape stable while making LRM usage explicitly opt-in.
