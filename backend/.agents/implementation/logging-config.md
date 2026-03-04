# Logging Configuration

`configure_logging()` establishes a queued logging pipeline for the backend. A
`QueueHandler` forwards records to a `QueueListener` which writes to a rotating
file handler stored under `backend/logs/backend.log`.

The file handler is wrapped in a timed memory buffer so log records are flushed
to disk roughly every 15 seconds. A `RichHandler` remains attached to the root
logger for colorful console output while the file handler receives buffered
records.
