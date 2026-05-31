"""The offline RuleModel must drive the classifier to sensible categories."""

from mailmind.classifiers import RuleModel
from mailmind.core.classifier import classify
from mailmind.domain import Category, Email


def _email(subject, body, sender="x@y.com"):
    return Email("m", "t", sender, ["me@y.com"], subject, body)


def test_detects_spam():
    m = RuleModel()
    r = classify(_email("You WON a prize", "Claim your $1000 gift card now"), m)
    assert r.category == Category.SPAM


def test_detects_urgent():
    m = RuleModel()
    r = classify(_email("[P1] Production down", "API returning 500s, page on-call"), m)
    assert r.category == Category.URGENT


def test_detects_newsletter():
    m = RuleModel()
    r = classify(_email("TLDR Weekly digest", "Top stories this week. Unsubscribe."), m)
    assert r.category == Category.NEWSLETTER


def test_defaults_to_action():
    m = RuleModel()
    r = classify(_email("Please review my PR", "Could you take a look when free?"), m)
    assert r.category == Category.ACTION


def test_bulk_sender_classified_as_newsletter_despite_content_word():
    # A newsletter from a bulk sender that happens to mention "production"
    # should still be a newsletter, not urgent.
    m = RuleModel()
    r = classify(
        _email("Top stories today", "News about production systems. Read more.",
               sender="News <news@cloud.google.com>"),
        m,
    )
    assert r.category == Category.NEWSLETTER


def test_classifies_entire_sample_corpus_correctly():
    from mailmind.core.email_parsing import parse_message
    from mailmind.sample_data import load_sample_emails

    m = RuleModel()
    expected = {"u": "urgent", "a": "action", "n": "newsletter", "s": "spam"}
    for raw in load_sample_emails():
        email = parse_message(raw)
        got = classify(email, m).category.value
        want = expected[email.id[0]]
        assert got == want, f"{email.id}: expected {want}, got {got}"
