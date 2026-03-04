# Backend discovery

The development server now resolves the backend URL when it starts. A Vite
plugin probes known container hostnames (`backend`, `backend-llm-*`) and
`localhost:59002`. The first reachable target becomes the API base and is
exposed via the `VITE_API_BASE` environment variable and an `/api-base` endpoint
served by the dev server.

Browser code no longer scans the network. `getApiBase()` reads the injected
`VITE_API_BASE` value or, in the browser, fetches the `/api-base` endpoint on the
development server. If neither path works, it falls back to
`http://localhost:59002`.

`BackendNotReady.svelte` now simply displays the unresolved API base and offers a
manual **Retry** button instead of polling the backend.
