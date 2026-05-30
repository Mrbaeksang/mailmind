"""Ingest raw Gmail messages into the store with embeddings."""

from __future__ import annotations

from collections.abc import Iterable

from mailmind.core.email_parsing import parse_message
from mailmind.core.embedding_input import embedding_input
from mailmind.core.ingest_transform import to_email_document
from mailmind.ports import EmbeddingModel
from mailmind.store import Store


def run_ingest(raw_messages: Iterable[dict], embedder: EmbeddingModel, store: Store) -> int:
    """Parse, embed, and upsert each message. Returns the number processed.

    Idempotent: documents are keyed by Gmail message id, so re-running upserts
    rather than duplicating.
    """
    count = 0
    for raw in raw_messages:
        email = parse_message(raw)
        vector = embedder.embed(embedding_input(email))
        store.upsert_email(to_email_document(email, vector))
        count += 1
    return count
