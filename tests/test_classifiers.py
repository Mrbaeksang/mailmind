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
