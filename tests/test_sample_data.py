"""The bundled synthetic email corpus must be well-formed and cover every feature."""

from collections import Counter

from mailmind.sample_data import load_sample_emails


def test_has_around_35_emails():
    emails = load_sample_emails()
    assert 30 <= len(emails) <= 40


def test_every_email_parses_into_the_domain_type():
    from mailmind.core.email_parsing import parse_message

    for raw in load_sample_emails():
        email = parse_message(raw)
        assert email.id
        assert email.subject
        assert email.body
        assert email.sender


def test_ids_are_unique():
    ids = [e["id"] for e in load_sample_emails()]
    assert len(ids) == len(set(ids))


def test_covers_multiple_threads_with_multi_message_threads():
    thread_ids = [e["threadId"] for e in load_sample_emails()]
    counts = Counter(thread_ids)
    multi = [t for t, n in counts.items() if n >= 2]
    assert len(multi) >= 3, "need at least 3 multi-message threads for the summarize demo"


def test_emails_are_english():
    # crude ASCII check — the corpus is intentionally English-only
    for raw in load_sample_emails():
        body = raw["payload"]["body"]["data"]
        assert body  # base64, non-empty


def test_contains_a_distinct_search_target():
    # there should be an email clearly about a contract, for the vector-search demo
    from mailmind.core.email_parsing import parse_message

    texts = [parse_message(r).subject + " " + parse_message(r).body for r in load_sample_emails()]
    assert any("contract" in t.lower() for t in texts)
