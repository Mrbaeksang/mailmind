"""Behavior of classifying an email into a triage category via a text model."""

from mailmind.core.classifier import classify
from mailmind.domain import Category, Email


class FakeModel:
    def __init__(self, response: str):
        self.response = response
        self.prompt: str | None = None

    def generate(self, prompt: str) -> str:
        self.prompt = prompt
        return self.response


def _email(subject="Server down", body="Production is on fire", sender="ops@x.com"):
    return Email(
        id="m1",
        thread_id="t1",
        sender=sender,
        recipients=["me@x.com"],
        subject=subject,
        body=body,
    )


def test_returns_category_and_confidence_from_model_json():
    model = FakeModel('{"category": "urgent", "confidence": 0.92}')

    result = classify(_email(), model)

    assert result.category == Category.URGENT
    assert result.confidence == 0.92


def test_parses_json_wrapped_in_markdown_fences():
    model = FakeModel('```json\n{"category": "spam", "confidence": 0.4}\n```')

    result = classify(_email(), model)

    assert result.category == Category.SPAM


def test_falls_back_to_action_on_unparseable_response():
    model = FakeModel("I think this is probably urgent, honestly.")

    result = classify(_email(), model)

    assert result.category == Category.ACTION
    assert result.confidence == 0.0


def test_prompt_includes_sender_subject_and_body():
    model = FakeModel('{"category": "action", "confidence": 0.5}')

    classify(_email(subject="Invoice 42", body="Please pay", sender="vendor@x.com"), model)

    assert "Invoice 42" in model.prompt
    assert "Please pay" in model.prompt
    assert "vendor@x.com" in model.prompt
