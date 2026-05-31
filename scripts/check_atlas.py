"""Smoke-test the live Atlas connection.

Verifies the connection string works and round-trips a document through the
real Store, then cleans it up. Run after filling MONGODB_URI in .env:

    uv run python scripts/check_atlas.py
"""

from __future__ import annotations

from mailmind.config import get_database, mongodb_db_name
from mailmind.store import Store


def main() -> None:
    db = get_database()
    db.command("ping")
    print(f"✓ Connected to Atlas database {mongodb_db_name()!r}")

    store = Store(db)
    probe = {
        "_id": "__smoke__",
        "threadId": "t0",
        "from": "smoke@test",
        "to": [],
        "subject": "smoke",
        "body": "smoke",
        "date": None,
        "category": None,
        "embedding": [0.0],
    }
    store.upsert_email(probe)
    found = [e for e in store.list_emails() if e["_id"] == "__smoke__"]
    print(f"✓ Round-tripped a document through Store (found={len(found)})")

    db["emails"].delete_one({"_id": "__smoke__"})
    print("✓ Cleaned up probe document. Atlas is ready.")


if __name__ == "__main__":
    main()
