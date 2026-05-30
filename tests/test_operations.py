"""Behavior of the app-level orchestration that the web layer injects.

These tie the core logic, store, and (eventually) the MCP tools together, but
depend only on injected callables so they run without live services.
"""

import mongomock

from mailmind.domain import Category, Classification, Email
from mailmind.operations import process_inbox, semantic_search
from mailmind.store import Store


def _email(_id="m1"):
    return Email(_id, "t1", "a@x.com", ["me@x.com"], "Subj", "Body")


def test_process_inbox_classifies_labels_and_persists_category():
    store = Store(mongomock.MongoClient().mailmind)
    store.upsert_email({"_id": "m1", "category": None})
    labelled = []

    def classify(email):
        return Classification(Category.URGENT, 0.9)

    def apply_label(email, category):
        labelled.append((email.id, category))

    count = process_inbox([_email("m1")], classify=classify, apply_label=apply_label, store=store)

    assert count == 1
    assert labelled == [("m1", Category.URGENT)]
    assert store.list_emails()[0]["category"] == "urgent"


def test_semantic_search_embeds_query_and_runs_vector_pipeline():
    seen_query = []
    seen_pipeline = []

    def embed(text):
        seen_query.append(text)
        return [0.5, 0.5]

    def run_aggregate(pipeline):
        seen_pipeline.append(pipeline)
        return [{"_id": "m1", "subject": "Contract"}]

    results = semantic_search("the contract email", embed=embed, run_aggregate=run_aggregate)

    assert seen_query == ["the contract email"]
    assert "$vectorSearch" in seen_pipeline[0][0]
    assert seen_pipeline[0][0]["$vectorSearch"]["queryVector"] == [0.5, 0.5]
    assert results[0]["_id"] == "m1"
