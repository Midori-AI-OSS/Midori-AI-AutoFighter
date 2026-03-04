# Logger

`src/lib/logger.js` ensures a `logs` directory exists and appends timestamped
messages to `logs/webui.log`. It exports `info`, `warn`, and `error` helpers
for server-side or development logging from Svelte components and scripts.
