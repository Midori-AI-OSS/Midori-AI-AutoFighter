from __future__ import annotations

import importlib
import os
from pathlib import Path
from typing import Dict


_HAS_DEPS = (
    importlib.util.find_spec("langchain_huggingface") is not None
    and importlib.util.find_spec("transformers") is not None
)

if _HAS_DEPS:  # pragma: no cover - optional heavy imports
    from langchain_huggingface import HuggingFacePipeline
    from transformers import pipeline


class LLMClient:
    """Minimal wrapper around a HuggingFace pipeline via LangChain."""

    def __init__(self, model_path: str | None = None) -> None:
        if not _HAS_DEPS:  # pragma: no cover - sanity guard
            raise RuntimeError("LangChain HuggingFace pipeline not available")
        model_id = model_path or os.getenv("AUTOFIGHTER_LLM_MODEL", "microsoft/phi-2")
        local_path = Path("llms") / model_id
        source = str(local_path) if local_path.exists() else model_id
        pipe = pipeline("text-generation", model=source, tokenizer=source)
        self.llm = HuggingFacePipeline(pipeline=pipe)
        self.history: Dict[str, list[str]] = {}

    @staticmethod
    def available() -> bool:
        """Return True if required libraries are installed."""

        return _HAS_DEPS

    def ask(self, character: str, message: str) -> str:
        """Return the model's reply and retain history per character."""

        history = self.history.setdefault(character, [])
        prompt = "\n".join(history + [f"User: {message}", "AI:"])
        reply = self.llm.invoke(prompt)
        history.extend([f"User: {message}", f"AI: {reply}"])
        return str(reply)


_CLIENT: LLMClient | None = None


def get_client(model_path: str | None = None) -> LLMClient:
    """Return a process-wide LLM client instance."""

    global _CLIENT
    if _CLIENT is None:
        _CLIENT = LLMClient(model_path)
    return _CLIENT

