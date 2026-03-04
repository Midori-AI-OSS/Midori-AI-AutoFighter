# LRM Memory Backend

The player and foe base classes use a lightweight memory layer to track chat history and, when available, a vector store for retrieval.

- Default: an internal in-process conversation memory that stores `(input, output)` pairs and serializes them into a simple "Human/AI" transcript. This avoids LangChain's deprecated memory APIs and emits no deprecation warnings.
- Vector store: if `langchain-community`, `langchain-chroma`, and `sentence-transformers` are installed (via `uv sync --extra llm-{cpu|cuda|amd}`), the memory upgrades to a `VectorStoreRetrieverMemory` backed by `Chroma` from the `langchain-chroma` package and `HuggingFaceEmbeddings`.

Notes
- The Chroma integration now imports `Chroma` from `langchain_chroma` (previously from `langchain_community.vectorstores`), aligning with LangChain 0.2+ guidance.
- If the vector store initialization fails at runtime, the code gracefully falls back to the internal memory without raising.

