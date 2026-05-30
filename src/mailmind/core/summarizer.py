"""Summarize a thread into a 3-line summary and a list of to-dos.

Prompt construction and response parsing are deterministic; the model call goes
through the TextModel port.
"""

from __future__ import annotations

from mailmind.core._json import extract_json_object
from mailmind.domain import Thread, ThreadInsight
from mailmind.ports import TextModel

_MAX_SUMMARY_LINES = 3


def build_prompt(thread: Thread) -> str:
    body = "\n\n---\n\n".join(
        f"From: {m.sender}\nSubject: {m.subject}\n\n{m.body}" for m in thread.messages
    )
    return (
        "Summarize this email thread in at most 3 short lines and extract concrete to-dos.\n"
        'Respond with JSON: {"summary": [<lines>], "todos": [<todos>]}.\n\n'
        f"{body}"
    )


def parse_insight(text: str) -> ThreadInsight:
    """Parse the model response, tolerating fences/prose; empty insight on failure."""
    data = extract_json_object(text)
    if data is not None:
        try:
            summary = [str(s) for s in data.get("summary", [])][:_MAX_SUMMARY_LINES]
            todos = [str(t) for t in data.get("todos", [])]
            return ThreadInsight(summary=summary, todos=todos)
        except (ValueError, TypeError):
            pass
    return ThreadInsight(summary=[], todos=[])


def summarize(thread: Thread, model: TextModel) -> ThreadInsight:
    response = model.generate(build_prompt(thread))
    return parse_insight(response)
