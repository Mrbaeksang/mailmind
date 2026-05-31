"""End-to-end smoke test of Atlas Vector Search against the live cluster.

Embeds a natural-language query with the same embedder used for ingestion and
runs the real $vectorSearch aggregation, printing the top hits. Requires that
load_samples.py has populated the corpus and the vector index is queryable.

    uv run python scripts/check_vector_search.py "the contract email"
"""

from __future__ import annotations

import json
import sys

from mailmind.config import embedding_dim, get_database
from mailmind.embedders import DummyEmbedder
from mailmind.operations import semantic_search
from mailmind.store import EMAILS


def main() -> None:
    query = sys.argv[1] if len(sys.argv) > 1 else "the vendor contract I need to sign"
    db = get_database()
    embedder = DummyEmbedder(dim=embedding_dim())

    def run_aggregate(pipeline: list[dict]) -> list[dict]:
        # add a projection so we don't pull back the big embedding vectors
        pipeline = pipeline + [
            {"$project": {"_id": 1, "subject": 1, "from": 1,
                          "score": {"$meta": "vectorSearchScore"}}}
        ]
        return list(db[EMAILS].aggregate(pipeline))

    results = semantic_search(query, embed=embedder.embed, run_aggregate=run_aggregate, limit=5)
    out = {"query": query, "hits": [
        {"id": r["_id"], "subject": r.get("subject", ""), "score": round(r.get("score", 0), 4)}
        for r in results
    ]}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
