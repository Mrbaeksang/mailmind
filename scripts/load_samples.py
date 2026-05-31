"""Load the synthetic email corpus into Atlas.

Uses the DummyEmbedder by default so it works WITHOUT Google Cloud. Once GCP is
configured, pass --vertex to use real Gemini embeddings instead.

    uv run python scripts/load_samples.py            # dummy (offline)
    uv run python scripts/load_samples.py --vertex   # real embeddings (needs GCP)
"""

from __future__ import annotations

import sys

from mailmind.config import embedding_dim, get_database
from mailmind.embedders import DummyEmbedder, VertexEmbedder
from mailmind.ingest.pipeline import run_ingest
from mailmind.sample_data import load_sample_emails
from mailmind.store import Store


def main() -> None:
    use_vertex = "--vertex" in sys.argv
    dim = embedding_dim()
    embedder = VertexEmbedder(dim=dim) if use_vertex else DummyEmbedder(dim=dim)

    store = Store(get_database())
    emails = load_sample_emails()
    count = run_ingest(emails, embedder, store)

    mode = "Vertex" if use_vertex else "Dummy"
    print(f"Ingested {count} emails into Atlas using {mode} embedder ({dim} dims).")


if __name__ == "__main__":
    main()
