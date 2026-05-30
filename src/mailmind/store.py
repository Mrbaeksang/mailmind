"""Direct (pymongo) access to the Atlas collections.

Used by the ingestion pipeline and the web read-APIs. The *agent* reaches Mongo
through the official MongoDB MCP server instead; this is the efficient path for
app code. The DB handle is injected so tests can run against an in-memory Mongo.
"""

from __future__ import annotations

from typing import Any

VECTOR_INDEX = "vector_index"
EMAILS = "emails"
THREADS = "threads"


class Store:
    def __init__(self, db: Any):
        self._db = db

    # --- emails ---------------------------------------------------------
    def upsert_email(self, doc: dict) -> None:
        self._db[EMAILS].replace_one({"_id": doc["_id"]}, doc, upsert=True)

    def list_emails(self, category: str | None = None) -> list[dict]:
        query = {"category": category} if category is not None else {}
        return list(self._db[EMAILS].find(query))

    def set_category(self, email_id: str, category: str) -> None:
        self._db[EMAILS].update_one({"_id": email_id}, {"$set": {"category": category}})

    # --- threads --------------------------------------------------------
    def save_thread_insight(
        self,
        thread_id: str,
        summary: list[str],
        todos: list[str],
        draft_id: str | None = None,
    ) -> None:
        self._db[THREADS].replace_one(
            {"_id": thread_id},
            {
                "_id": thread_id,
                "summary": summary,
                "todos": todos,
                "draftId": draft_id,
            },
            upsert=True,
        )

    def get_thread_insight(self, thread_id: str) -> dict | None:
        return self._db[THREADS].find_one({"_id": thread_id})

    # --- vector search --------------------------------------------------
    @staticmethod
    def build_vector_search_pipeline(
        query_vector: list[float], limit: int = 5, category: str | None = None
    ) -> list[dict]:
        """Build the Atlas ``$vectorSearch`` aggregation pipeline.

        This is the exact payload the agent issues via the MongoDB MCP
        ``aggregate`` tool; kept pure so its shape is unit-testable.
        """
        stage: dict = {
            "index": VECTOR_INDEX,
            "path": "embedding",
            "queryVector": query_vector,
            "numCandidates": max(limit * 10, 100),
            "limit": limit,
        }
        if category is not None:
            stage["filter"] = {"category": category}
        return [{"$vectorSearch": stage}]
