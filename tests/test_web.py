"""Behavior of the FastAPI HTTP layer (verified with TestClient + fakes)."""

import mongomock
import pytest
from fastapi.testclient import TestClient

from mailmind.store import Store
from mailmind.web.app import create_app


def _email_doc(_id="m1", category="urgent"):
    return {
        "_id": _id,
        "threadId": "t1",
        "from": "a@x.com",
        "to": ["me@x.com"],
        "subject": "Hi",
        "body": "hello",
        "date": None,
        "category": category,
        "embedding": [0.1, 0.2, 0.3],
    }


@pytest.fixture
def store():
    return Store(mongomock.MongoClient().mailmind)


def test_health_ok(store):
    client = TestClient(create_app(store))
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_list_emails_omits_embedding(store):
    store.upsert_email(_email_doc())
    client = TestClient(create_app(store))

    resp = client.get("/emails")

    assert resp.status_code == 200
    body = resp.json()
    assert body[0]["_id"] == "m1"
    assert "embedding" not in body[0]


def test_list_emails_filters_by_category(store):
    store.upsert_email(_email_doc("m1", category="urgent"))
    store.upsert_email(_email_doc("m2", category="spam"))
    client = TestClient(create_app(store))

    resp = client.get("/emails", params={"category": "spam"})

    assert [e["_id"] for e in resp.json()] == ["m2"]


def test_get_thread_returns_insight(store):
    store.save_thread_insight("t1", summary=["s"], todos=["t"], draft_id="d1")
    client = TestClient(create_app(store))

    resp = client.get("/threads/t1")

    assert resp.status_code == 200
    assert resp.json()["summary"] == ["s"]


def test_get_missing_thread_is_404(store):
    client = TestClient(create_app(store))
    assert client.get("/threads/nope").status_code == 404


def test_process_invokes_injected_processor(store):
    calls = []

    def processor():
        calls.append(True)
        return 5

    client = TestClient(create_app(store, processor=processor))

    resp = client.post("/process")

    assert resp.status_code == 200
    assert resp.json()["processed"] == 5
    assert calls == [True]


def test_search_passes_query_to_searcher(store):
    seen = []

    def searcher(q):
        seen.append(q)
        return [{"_id": "m1", "subject": "Hi"}]

    client = TestClient(create_app(store, searcher=searcher))

    resp = client.get("/search", params={"q": "contract email"})

    assert resp.status_code == 200
    assert seen == ["contract email"]
    assert resp.json()[0]["_id"] == "m1"
