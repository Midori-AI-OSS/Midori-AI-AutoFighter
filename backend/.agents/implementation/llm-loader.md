# LLM Loader

The loader in `backend/llms/loader.py` wraps several LangChain-compatible backends behind a single streaming interface.

## Supported Models
- `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B`
- `google/gemma-3-4b-it`
- `gguf` models via `llama.cpp`

## Configuration
- `AF_LLM_MODEL` selects the backend. It defaults to the DeepSeek model.
- `AF_GGUF_PATH` provides the path to the GGUF file when using `gguf`.

`load_llm()` returns an object exposing `async generate_stream(text: str) -> AsyncIterator[str]`.

Optional dependencies such as PyTorch and Transformers are imported lazily. If
these packages are absent, `load_llm()` raises a `RuntimeError` when called
instead of failing during module import, allowing the rest of the backend to
run without LLM features.

## Resource Checks

`backend/llms/safety.py` inspects available system memory and GPU VRAM before
loading a model. Memory requirements for Hugging Face models are derived from
the reported weight file sizes, removing the need for hard‑coded numbers. When a
GPU is present the Hugging Face pipeline uses `device_map="auto"` so layers that
do not fit in VRAM are automatically offloaded to system RAM. When overall RAM
is insufficient a `RuntimeError` is raised with a descriptive message. GGUF
models estimate requirements from the file size and compute how many layers to
run on the GPU based on available VRAM, sharding the remainder to the CPU.
