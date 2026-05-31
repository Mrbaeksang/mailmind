"""Run the classify→persist pipeline over the corpus already in Atlas.

Offline by default: uses RuleModel and a no-op label applier (real Gmail
labeling needs the Gmail MCP). Proves process_inbox + category persistence
against the live database.

    uv run python scripts/process_inbox.py
"""

from __future__ import annotations

import json

from mailmind.classifiers import RuleModel
from mailmind.config import get_database
from mailmind.core.email_parsing import parse_message
from mailmind.domain import Category, Email
from mailmind.operations import process_inbox
from mailmind.sample_data import load_sample_emails
from mailmind.store import Store


def main() -> None:
    store = Store(get_database())
    model = RuleModel()
    emails = [parse_message(r) for r in load_sample_emails()]

    applied: list[tuple[str, str]] = []

    def classify(email: Email):
        from mailmind.core.classifier import classify as _classify

        return _classify(email, model)

    def apply_label(email: Email, category: Category) -> None:
        # offline stand-in for the Gmail MCP label_message call
        applied.append((email.id, category.value))

    count = process_inbox(emails, classify=classify, apply_label=apply_label, store=store)

    # report category distribution as persisted in Atlas
    dist: dict[str, int] = {}
    for doc in store.list_emails():
        c = doc.get("category") or "none"
        dist[c] = dist.get(c, 0) + 1
    print(json.dumps({"processed": count, "labels_applied": len(applied),
                      "persisted_distribution": dist}, indent=2))


if __name__ == "__main__":
    main()
