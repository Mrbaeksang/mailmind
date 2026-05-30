"""Behavior of the ingestion pipeline (parse → embed → store)."""

import base64

import mongomock
import pytest

from mailmind.ingest.pipeline import run_ingest
from mailmind.store import Store


class FakeEmbedder:
    def __init__(self):
        self.seen: list[str] = []

    def embed(self, text: str) -> list[float]:
        self.seen.append(text)
        return [float(len(text))]


@pytest.fixture
def store():
    return Store(mongomock.MongoClient().mailmind)


def _raw(_id="m1", subject="Hi", body="hello"):
    return {
        "id": _id,
        "threadId": "t1",
        "payload": {
            "mimeType": "text/plain",
            "headers": [{"name": "Subject", "value": subject}],
            "body": {"data": base64.urlsafe_b64encode(body.encode()).decode()},
        },
    }


def test_ingest_stores_a_document_per_message(store):
    count = run_ingest([_raw("m1"), _raw("m2")], FakeEmbedder(), store)

    assert count == 2
    assert {e["_id"] for e in store.list_emails()} == {"m1", "m2"}


def test_ingested_documents_carry_an_embedding(store):
    run_ingest([_raw("m1", body="hello world")], FakeEmbedder(), store)

    [doc] = store.list_emails()
    assert isinstance(doc["embedding"], list) and doc["embedding"]


def test_ingest_is_idempotent(store):
    run_ingest([_raw("m1")], FakeEmbedder(), store)
    run_ingest([_raw("m1")], FakeEmbedder(), store)

    assert len(store.list_emails()) == 1


def test_ingest_embeds_subject_and_body_not_sender():
    embedder = FakeEmbedder()
    store = Store(mongomock.MongoClient().mailmind)

    run_ingest([_raw("m1", subject="Quarterly", body="numbers")], embedder, store)

    assert any("Quarterly" in t and "numbers" in t for t in embedder.seen)
