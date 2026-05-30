"""Behavior of turning an Email + embedding into an Atlas `emails` document."""

from mailmind.core.ingest_transform import to_email_document
from mailmind.domain import Category, Email


def _email():
    return Email(
        id="m1",
        thread_id="t1",
        sender="Alice <alice@example.com>",
        recipients=["me@example.com"],
        subject="Lunch?",
        body="Free today?",
        date="2026-05-30T00:00:00+00:00",
    )


def test_builds_document_with_email_fields_and_embedding():
    doc = to_email_document(_email(), [0.1, 0.2, 0.3])

    assert doc["_id"] == "m1"
    assert doc["threadId"] == "t1"
    assert doc["from"] == "Alice <alice@example.com>"
    assert doc["subject"] == "Lunch?"
    assert doc["body"] == "Free today?"
    assert doc["date"] == "2026-05-30T00:00:00+00:00"
    assert doc["embedding"] == [0.1, 0.2, 0.3]
    assert doc["category"] is None


def test_stores_category_as_string_value():
    doc = to_email_document(_email(), [0.1], category=Category.URGENT)

    assert doc["category"] == "urgent"
