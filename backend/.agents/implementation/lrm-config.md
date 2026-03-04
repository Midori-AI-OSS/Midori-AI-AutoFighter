# LRM Configuration

The configuration routes expose and persist language reasoning model choices.

## Endpoints
- `GET /config/lrm` returns the current model and the list of available `ModelName` values.
- `POST /config/lrm` persists the selected model string in the `options` table.
- `POST /config/lrm/test` runs the stored model on a provided prompt without memory and returns the raw reply.

The import of `load_llm` is deferred inside the `/config/lrm/test` endpoint so
the other configuration routes remain operational even when optional LLM
dependencies are missing.

## Chat Rooms
`ChatRoom.resolve()` reads the persisted model via `options.get_option`, loads it with `load_llm`, and sends the user's message and serialized party context to the model. The LRM's reply is returned as `response` alongside existing room data.
