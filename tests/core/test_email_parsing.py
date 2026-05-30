"""Behavior of parsing raw Gmail API message resources into the Email domain type."""

import base64

from mailmind.core.email_parsing import parse_message, parse_thread


def _b64(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode()).decode()


def _message(*, headers, body_data=None, parts=None, mime="text/plain", **extra):
    payload = {"mimeType": mime, "headers": headers}
    if body_data is not None:
        payload["body"] = {"data": _b64(body_data)}
    if parts is not None:
        payload["parts"] = parts
    return {"id": "m1", "threadId": "t1", "payload": payload, **extra}


def test_prefers_plain_text_part_in_multipart_message():
    raw = _message(
        mime="multipart/alternative",
        headers=[{"name": "Subject", "value": "Newsletter"}],
        parts=[
            {"mimeType": "text/html", "body": {"data": _b64("<p>HTML version</p>")}},
            {"mimeType": "text/plain", "body": {"data": _b64("Plain version")}},
        ],
    )

    email = parse_message(raw)

    assert email.body == "Plain version"


def test_parses_thread_into_ordered_messages():
    m1 = _message(headers=[{"name": "Subject", "value": "First"}], body_data="one")
    m2 = _message(headers=[{"name": "Subject", "value": "Re: First"}], body_data="two")
    m2["id"] = "m2"
    raw_thread = {"id": "t1", "messages": [m1, m2]}

    thread = parse_thread(raw_thread)

    assert thread.id == "t1"
    assert [m.id for m in thread.messages] == ["m1", "m2"]
    assert thread.messages[1].subject == "Re: First"


def test_derives_iso_date_from_internal_date():
    raw = _message(
        headers=[{"name": "Subject", "value": "x"}],
        body_data="hi",
        internalDate="1700000000000",
    )

    email = parse_message(raw)

    assert email.date is not None
    assert email.date.startswith("2023-11-")


def test_parses_plain_text_message():
    raw = _message(
        headers=[
            {"name": "From", "value": "Alice <alice@example.com>"},
            {"name": "To", "value": "me@example.com"},
            {"name": "Subject", "value": "Lunch?"},
        ],
        body_data="Are you free for lunch?",
    )

    email = parse_message(raw)

    assert email.id == "m1"
    assert email.thread_id == "t1"
    assert email.subject == "Lunch?"
    assert email.sender == "Alice <alice@example.com>"
    assert email.body == "Are you free for lunch?"
