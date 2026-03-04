# LRM Memory Notes

The previous LangChain/Chroma memory stack is not part of the active backend
runtime path.

Current foundation behavior is intentionally minimal:

- Chat replies are one-shot requests through the configured LRM provider.
- No persistent vector-memory layer is required for the current backend flow.
- On provider failure or disabled mode, responses degrade to empty text.

If long-term conversation memory is reintroduced later, document the storage
model and failure semantics alongside the runtime implementation.
