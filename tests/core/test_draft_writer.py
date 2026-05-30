"""Behavior of composing a reply draft for a thread in a given tone."""

from mailmind.core.draft_writer import compose_reply
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
            Email("m1", "t1", "alice@x.com", ["me@x.com"], "Lunch?", "Are you free Friday?"),
        ],
    )


def test_returns_stripped_draft_text():
    model = FakeModel("\n  Sure, Friday works for me!  \n")

    draft = compose_reply(_thread(), tone="friendly and brief", model=model)

    assert draft == "Sure, Friday works for me!"


def test_prompt_includes_tone_and_latest_message():
    model = FakeModel("ok")

    compose_reply(_thread(), tone="formal and concise", model=model)

    assert "formal and concise" in model.prompt
    assert "Are you free Friday?" in model.prompt
