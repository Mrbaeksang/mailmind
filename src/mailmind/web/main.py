"""Composition root: build the FastAPI app wired to live resources.

Offline-friendly: classification uses RuleModel and search uses DummyEmbedder
unless GCP is configured. Swap to GeminiModel / VertexEmbedder once GOOGLE_CLOUD_*
is set. Gmail labeling is a no-op until the Gmail MCP is wired.

    uv run uvicorn mailmind.web.main:app --reload
"""

from __future__ import annotations

from mailmind.classifiers import RuleModel
from mailmind.config import embedding_dim, get_database
from mailmind.core.classifier import classify as _classify
from mailmind.core.email_parsing import parse_message
from mailmind.domain import Category, Email
from mailmind.embedders import DummyEmbedder
from mailmind.operations import process_inbox, semantic_search
from mailmind.sample_data import load_sample_emails
from mailmind.store import EMAILS, Store
from mailmind.web.app import create_app


def build_app():
    db = get_database()
    store = Store(db)
    model = RuleModel()
    embedder = DummyEmbedder(dim=embedding_dim())

    def processor() -> int:
        emails = [parse_message(r) for r in load_sample_emails()]

        def classify(e: Email):
            return _classify(e, model)

        def apply_label(_e: Email, _c: Category) -> None:
            pass  # Gmail MCP label call goes here once wired

        return process_inbox(emails, classify=classify, apply_label=apply_label, store=store)

    def searcher(q: str) -> list[dict]:
        def run_aggregate(pipeline: list[dict]) -> list[dict]:
            pipeline = pipeline + [
                {"$project": {"_id": 1, "subject": 1, "from": 1, "category": 1,
                              "score": {"$meta": "vectorSearchScore"}}}
            ]
            return list(db[EMAILS].aggregate(pipeline))

        return semantic_search(q, embed=embedder.embed, run_aggregate=run_aggregate, limit=5)

    return create_app(store, processor=processor, searcher=searcher)


app = build_app()
