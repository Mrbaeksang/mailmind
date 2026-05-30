"""Behavior of the Atlas-backed store (verified with an in-memory Mongo)."""

import mongomock
import pytest

from mailmind.store import Store


@pytest.fixture
def store():
    db = mongomock.MongoClient().mailmind
    return Store(db)


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


def test_upsert_then_list_returns_the_email(store):
    store.upsert_email(_email_doc())

    emails = store.list_emails()

    assert [e["_id"] for e in emails] == ["m1"]


def test_upsert_is_idempotent_on_id(store):
    store.upsert_email(_email_doc(category="urgent"))
    store.upsert_email(_email_doc(category="action"))  # same _id, new category

    emails = store.list_emails()

    assert len(emails) == 1
    assert emails[0]["category"] == "action"


def test_list_emails_filters_by_category(store):
    store.upsert_email(_email_doc("m1", category="urgent"))
    store.upsert_email(_email_doc("m2", category="spam"))

    urgent = store.list_emails(category="urgent")

    assert [e["_id"] for e in urgent] == ["m1"]


def test_thread_insight_round_trips(store):
    store.save_thread_insight("t1", summary=["s1", "s2"], todos=["do x"], draft_id="d1")

    insight = store.get_thread_insight("t1")

    assert insight["summary"] == ["s1", "s2"]
    assert insight["todos"] == ["do x"]
    assert insight["draftId"] == "d1"


def test_get_missing_thread_insight_returns_none(store):
    assert store.get_thread_insight("nope") is None


def test_vector_search_pipeline_has_expected_shape():
    pipeline = Store.build_vector_search_pipeline([0.1, 0.2], limit=7)

    stage = pipeline[0]["$vectorSearch"]
    assert stage["path"] == "embedding"
    assert stage["queryVector"] == [0.1, 0.2]
    assert stage["limit"] == 7


def test_vector_search_pipeline_applies_category_prefilter():
    pipeline = Store.build_vector_search_pipeline([0.1], limit=5, category="urgent")

    assert pipeline[0]["$vectorSearch"]["filter"] == {"category": "urgent"}
