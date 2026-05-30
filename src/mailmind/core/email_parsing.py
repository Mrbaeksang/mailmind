"""Parse raw Gmail API message resources into the Email domain type."""

from __future__ import annotations

import base64
from datetime import UTC, datetime

from mailmind.domain import Email, Thread


def _header(headers: list[dict], name: str) -> str:
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def _decode(data: str) -> str:
    return base64.urlsafe_b64decode(data.encode()).decode("utf-8", errors="replace")


def _extract_body(payload: dict) -> str:
    """Return the plain-text body, preferring text/plain over any other part."""
    data = payload.get("body", {}).get("data")
    if data and payload.get("mimeType", "").startswith("text/plain"):
        return _decode(data)

    parts = payload.get("parts", [])
    for part in parts:
        if part.get("mimeType", "").startswith("text/plain"):
            inner = part.get("body", {}).get("data")
            if inner:
                return _decode(inner)
    # nested multipart: recurse
    for part in parts:
        nested = _extract_body(part)
        if nested:
            return nested
    # last resort: a top-level non-multipart body
    if data:
        return _decode(data)
    return ""


def _date(raw: dict, headers: list[dict]) -> str | None:
    internal = raw.get("internalDate")
    if internal:
        return datetime.fromtimestamp(int(internal) / 1000, tz=UTC).isoformat()
    return _header(headers, "Date") or None


def parse_message(raw: dict) -> Email:
    payload = raw.get("payload", {})
    headers = payload.get("headers", [])
    body = _extract_body(payload)
    return Email(
        id=raw.get("id", ""),
        thread_id=raw.get("threadId", ""),
        sender=_header(headers, "From"),
        recipients=[_header(headers, "To")] if _header(headers, "To") else [],
        subject=_header(headers, "Subject"),
        body=body,
        date=_date(raw, headers),
    )


def parse_thread(raw_thread: dict) -> Thread:
    messages = [parse_message(m) for m in raw_thread.get("messages", [])]
    return Thread(id=raw_thread.get("id", ""), messages=messages)
