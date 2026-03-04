# Status Endpoint

- `GET /` responds with `{ "status": "ok", "flavor": "default" }`.
- The `flavor` field reflects the `UV_EXTRA` environment variable, defaulting to `"default"`.
