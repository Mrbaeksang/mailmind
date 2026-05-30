"""App-level orchestration wired at the composition root.

Each function depends on injected callables (classify, apply_label, embed,
run_aggregate) which the deployment binds to the real Gemini model, the Gmail
MCP tools, and the MongoDB MCP ``aggregate`` tool. Keeping them injected makes
the orchestration testable without any live service.
"""

from __future__ import annotations

from collections.abc import Callable

from mailmind.domain import Category, Classification, Email
from mailmind.store import Store


def process_inbox(
    emails: list[Email],
    classify: Callable[[Email], Classification],
    apply_label: Callable[[Email, Category], None],
    store: Store,
) -> int:
    """Classify each email, apply its Gmail label, and persist the category."""
    count = 0
    for email in emails:
        category = classify(email).category
        apply_label(email, category)
        store.set_category(email.id, category)
        count += 1
    return count


def semantic_search(
    query: str,
    embed: Callable[[str], list[float]],
    run_aggregate: Callable[[list[dict]], list[dict]],
    limit: int = 5,
    category: str | None = None,
) -> list[dict]:
    """Embed the query and run the Atlas ``$vectorSearch`` pipeline via MCP."""
    vector = embed(query)
    pipeline = Store.build_vector_search_pipeline(vector, limit=limit, category=category)
    return run_aggregate(pipeline)
