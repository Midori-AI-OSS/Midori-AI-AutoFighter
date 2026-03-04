# Event and Chat Rooms

`EventRoom` presents deterministic text events with selectable outcomes. Each option applies its effect immediately and returns to map flow.

`ChatRoom` supports optional one-shot dialogue via backend LRM provider settings:

- If provider is `codex_cli`, the backend submits a single prompt to Codex CLI and returns the reply.
- If provider is `disabled` or execution fails, the backend returns an empty response and run flow continues safely.

Chat room handling is intentionally fail-safe and should never block progression on LRM errors.
