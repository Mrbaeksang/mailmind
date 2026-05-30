"""Compose a reply draft for a thread in the user's tone.

Tone is supplied as a short natural-language description and woven into the
prompt; the model call goes through the TextModel port. Output is draft text
only — saving it as a Gmail draft (never sending) happens in an adapter.
"""

from __future__ import annotations

from mailmind.domain import Thread
from mailmind.ports import TextModel


def build_prompt(thread: Thread, tone: str) -> str:
    conversation = "\n\n---\n\n".join(
        f"From: {m.sender}\nSubject: {m.subject}\n\n{m.body}" for m in thread.messages
    )
    return (
        "Write a reply to the latest message in this email thread.\n"
        f"Match this tone: {tone}.\n"
        "Return only the reply body text, no preamble.\n\n"
        f"{conversation}"
    )


def compose_reply(thread: Thread, tone: str, model: TextModel) -> str:
    response = model.generate(build_prompt(thread, tone))
    return response.strip()
