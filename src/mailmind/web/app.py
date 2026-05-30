"""FastAPI application factory.

Agent-backed operations are passed in as callables so the HTTP layer can be
tested without a live agent / MCP servers. Wiring the real agent happens at the
composition root (deployment). Rate-limiting the process action is an S7 concern.
"""

from __future__ import annotations

from collections.abc import Callable

from fastapi import FastAPI, HTTPException

from mailmind.store import Store

Processor = Callable[[], int]
Searcher = Callable[[str], list[dict]]


def _public(email: dict) -> dict:
    """Email shape for the UI — drop the heavy embedding vector."""
    return {k: v for k, v in email.items() if k != "embedding"}


def create_app(
    store: Store,
    processor: Processor | None = None,
    searcher: Searcher | None = None,
) -> FastAPI:
    app = FastAPI(title="MailMind")

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.get("/emails")
    def list_emails(category: str | None = None) -> list[dict]:
        return [_public(e) for e in store.list_emails(category=category)]

    @app.get("/threads/{thread_id}")
    def get_thread(thread_id: str) -> dict:
        insight = store.get_thread_insight(thread_id)
        if insight is None:
            raise HTTPException(status_code=404, detail="thread not found")
        return insight

    @app.post("/process")
    def process() -> dict:
        if processor is None:
            raise HTTPException(status_code=503, detail="processor not configured")
        return {"processed": processor()}

    @app.get("/search")
    def search(q: str) -> list[dict]:
        if searcher is None:
            raise HTTPException(status_code=503, detail="search not configured")
        return searcher(q)

    return app
