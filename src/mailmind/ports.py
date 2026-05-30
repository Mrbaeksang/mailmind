"""Narrow ports the core logic depends on, so the LLM/embeddings stay mockable.

Adapters (Vertex/Gemini) implement these; core modules only see the Protocol.
"""

from __future__ import annotations

from typing import Protocol


class TextModel(Protocol):
    """Generates text from a prompt (e.g. Gemini)."""

    def generate(self, prompt: str) -> str: ...


class EmbeddingModel(Protocol):
    """Turns text into an embedding vector (e.g. Vertex gemini-embedding-001)."""

    def embed(self, text: str) -> list[float]: ...
