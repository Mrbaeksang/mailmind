"""Embedding adapters implementing the EmbeddingModel port.

- DummyEmbedder: deterministic, dependency-free, word-overlap-driven. Lets us
  exercise the full Atlas vector-search path WITHOUT Google Cloud credentials.
- VertexEmbedder: the real Gemini Embedding model (used once GCP is set up).

Both return plain ``list[float]`` so ingestion/store don't care which is used.
"""

from __future__ import annotations

import hashlib
import math
import re

_TOKEN = re.compile(r"[a-z0-9]+")


class DummyEmbedder:
    """A hashing bag-of-words embedder.

    Each token is hashed into a bucket; shared tokens land in shared dimensions,
    so texts with overlapping words have higher cosine similarity. Deterministic
    and offline — meant for local/dev and CI, not production quality.
    """

    def __init__(self, dim: int = 3072):
        self.dim = dim

    def embed(self, text: str) -> list[float]:
        vec = [0.0] * self.dim
        for token in _TOKEN.findall(text.lower()):
            h = int(hashlib.md5(token.encode()).hexdigest(), 16)
            idx = h % self.dim
            sign = 1.0 if (h >> 8) & 1 else -1.0
            vec[idx] += sign
        norm = math.sqrt(sum(x * x for x in vec))
        if norm == 0.0:
            # empty/blank text → a stable nonzero unit vector
            vec[0] = 1.0
            return vec
        return [x / norm for x in vec]


class VertexEmbedder:
    """Real embeddings via Vertex AI Gemini Embedding.

    Imported lazily so the rest of the app runs without google-genai installed
    or GCP configured. Wire this in once GOOGLE_CLOUD_PROJECT / ADC are set.
    """

    def __init__(self, model: str = "gemini-embedding-2", dim: int = 3072):
        self.model = model
        self.dim = dim

    def embed(self, text: str) -> list[float]:  # pragma: no cover - needs GCP
        from google import genai

        client = genai.Client(vertexai=True)
        resp = client.models.embed_content(
            model=self.model,
            contents=text,
            config={"output_dimensionality": self.dim},
        )
        return list(resp.embeddings[0].values)
