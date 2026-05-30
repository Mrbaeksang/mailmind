"""Build the canonical text to embed for an email.

Subject + body only; the sender is kept as structured metadata elsewhere so it
does not dilute semantic similarity.
"""

from __future__ import annotations

import re

from mailmind.domain import Email

_WHITESPACE = re.compile(r"\s+")


def _clean(text: str) -> str:
    return _WHITESPACE.sub(" ", text).strip()


def embedding_input(email: Email, max_chars: int = 8000) -> str:
    text = f"{_clean(email.subject)}\n\n{_clean(email.body)}"
    return text[:max_chars]
