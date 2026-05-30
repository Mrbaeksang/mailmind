"""Behavior of summarizing a thread into a 3-line summary + to-dos."""

from mailmind.core.summarizer import summarize
from mailmind.domain import Email, Thread


class FakeModel:
    def __init__(self, response: str):
        self.response = response
        self.prompt: str | None = None

    def generate(self, prompt: str) -> str:
        self.prompt = prompt
        return self.response


def _thread():
    return Thread(
        id="t1",
        messages=[
            Email("m1", "t1", "a@x.com", ["me@x.com"], "Budget", "Need approval by Friday."),
            Email("m2", "t1", "me@x.com", ["a@x.com"], "Re: Budget", "Will review tomorrow."),
        ],
    )


def test_returns_summary_and_todos_from_model_json():
    model = FakeModel(
        '{"summary": ["Budget needs approval", "Due Friday", "Reviewer will look tomorrow"],'
        ' "todos": ["Approve the budget", "Review by tomorrow"]}'
    )

    insight = summarize(_thread(), model)

    assert insight.summary == ["Budget needs approval", "Due Friday", "Reviewer will look tomorrow"]
    assert insight.todos == ["Approve the budget", "Review by tomorrow"]


def test_caps_summary_at_three_lines():
    model = FakeModel('{"summary": ["a", "b", "c", "d", "e"], "todos": []}')

    insight = summarize(_thread(), model)

    assert len(insight.summary) == 3


def test_falls_back_to_empty_insight_on_unparseable_response():
    model = FakeModel("sorry, I cannot do that")

    insight = summarize(_thread(), model)

    assert insight.summary == []
    assert insight.todos == []


def test_prompt_includes_message_bodies():
    model = FakeModel('{"summary": [], "todos": []}')

    summarize(_thread(), model)

    assert "Need approval by Friday." in model.prompt
    assert "Will review tomorrow." in model.prompt
