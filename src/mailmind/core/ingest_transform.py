"""Turn an Email + its embedding into an Atlas `emails` collection document.

`_id` is the Gmail message id so re-ingesting upserts rather than duplicating.
"""

from __future__ import annotations

from mailmind.domain import Category, Email


def to_email_document(
    email: Email, embedding: list[float], category: Category | None = None
) -> dict:
    return {
        "_id": email.id,
        "threadId": email.thread_id,
        "from": email.sender,
        "to": email.recipients,
        "subject": email.subject,
        "body": email.body,
        "date": email.date,
        "category": category.value if category is not None else None,
        "embedding": embedding,
    }
