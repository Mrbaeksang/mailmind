"""Runtime configuration loaded from environment (.env for local dev).

Secrets live only in the environment / Secret Manager — never in code. This
module reads them and hands back connected resources.
"""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

EMAILS_VECTOR_INDEX = "vector_index"
DEFAULT_EMBEDDING_DIM = 3072


def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Missing required env var {name!r}. Copy .env.example to .env and fill it in."
        )
    return value


def mongodb_uri() -> str:
    return _require("MONGODB_URI")


def mongodb_db_name() -> str:
    return os.environ.get("MONGODB_DB", "mailmind")


def embedding_dim() -> int:
    return int(os.environ.get("EMBEDDING_DIM", DEFAULT_EMBEDDING_DIM))


@lru_cache(maxsize=1)
def get_database():
    """Return a connected pymongo Database (cached). Imports pymongo lazily."""
    from pymongo import MongoClient

    client = MongoClient(mongodb_uri())
    return client[mongodb_db_name()]
