"""Behavior of building the canonical text that gets embedded for an email."""

from mailmind.core.embedding_input import embedding_input
from mailmind.domain import Email


def _email(subject="Subject", body="Body", sender="alice@example.com"):
    return Email(
        id="m1",
        thread_id="t1",
        sender=sender,
        recipients=["me@example.com"],
        subject=subject,
        body=body,
    )


def test_combines_subject_and_body_excluding_sender():
    text = embedding_input(_email(subject="Quarterly report", body="Numbers attached."))

    assert "Quarterly report" in text
    assert "Numbers attached." in text
    assert "alice@example.com" not in text


def test_collapses_whitespace_and_trims():
    text = embedding_input(_email(subject="  Hi  ", body="a\n\n\nb   c"))

    assert text == "Hi\n\na b c"


def test_truncates_to_max_chars():
    text = embedding_input(_email(subject="S", body="word " * 5000), max_chars=100)

    assert len(text) <= 100
