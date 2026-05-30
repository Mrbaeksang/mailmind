"""Tolerant extraction of a single JSON object from a model response.

Models often wrap JSON in markdown fences or surrounding prose; this finds the
first ``{...}`` block and parses it, returning None on failure so callers can
apply their own fallback.
"""

from __future__ import annotations

import json
import re

_JSON_OBJECT = re.compile(r"\{.*\}", re.DOTALL)


def extract_json_object(text: str) -> dict | None:
    match = _JSON_OBJECT.search(text)
    if not match:
        return None
    try:
        data = json.loads(match.group(0))
    except ValueError:
        return None
    return data if isinstance(data, dict) else None
