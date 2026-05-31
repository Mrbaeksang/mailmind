"""Create the Atlas Vector Search index on emails.embedding.

Idempotent: skips creation if an index with the same name already exists.
Run once after the cluster + collection exist:

    uv run python scripts/create_vector_index.py
"""

from __future__ import annotations

from pymongo.operations import SearchIndexModel

from mailmind.config import EMAILS_VECTOR_INDEX, embedding_dim, get_database
from mailmind.store import EMAILS


def main() -> None:
    db = get_database()
    collection = db[EMAILS]

    existing = {idx["name"] for idx in collection.list_search_indexes()}
    if EMAILS_VECTOR_INDEX in existing:
        print(f"Vector index {EMAILS_VECTOR_INDEX!r} already exists — nothing to do.")
        return

    model = SearchIndexModel(
        name=EMAILS_VECTOR_INDEX,
        type="vectorSearch",
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding",
                    "numDimensions": embedding_dim(),
                    "similarity": "cosine",
                },
                {"type": "filter", "path": "category"},
            ]
        },
    )
    collection.create_search_index(model=model)
    print(
        f"Created vector index {EMAILS_VECTOR_INDEX!r} on {EMAILS}.embedding "
        f"({embedding_dim()} dims, cosine). It may take a minute to build."
    )


if __name__ == "__main__":
    main()
