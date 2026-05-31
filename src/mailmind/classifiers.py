"""TextModel adapters for classification/summarization/drafting.

- RuleModel: offline, keyword-driven stand-in for Gemini. Returns the same JSON
  shape the core parsers expect, so the full classify/summarize path runs
  without Google Cloud.
- GeminiModel: real Gemini via Vertex (wired once GCP is set up).
"""

from __future__ import annotations

import json

_URGENT = ("urgent", "p1", "asap", "immediately", "today", "deadline", "rotate", "leaked",
           "incident", "500s", "production")
_SPAM = ("won", "winner", "prize", "lottery", "gift card", "crypto", "100x", "no prescription",
         "inheritance", "claim", "$1000", "deactivated", "verify your account")
_NEWSLETTER = ("newsletter", "weekly", "digest", "briefing", "tldr", "what's new",
               "this week", "this month", "unsubscribe")


class RuleModel:
    """Keyword heuristic that emits the model JSON contract (offline)."""

    def generate(self, prompt: str) -> str:
        # The prompt's instruction lists the category names ("urgent, action,
        # ...") — scan only the email content (after "From:") to avoid matching
        # those labels.
        marker = prompt.find("From:")
        text = (prompt[marker:] if marker != -1 else prompt).lower()

        def hits(words):
            return sum(1 for w in words if w in text)

        spam, urgent, news = hits(_SPAM), hits(_URGENT), hits(_NEWSLETTER)
        if spam >= 1 and spam >= urgent:
            cat, conf = "spam", 0.8
        elif urgent >= 1:
            cat, conf = "urgent", 0.75
        elif news >= 1:
            cat, conf = "newsletter", 0.7
        else:
            cat, conf = "action", 0.6
        return json.dumps({"category": cat, "confidence": conf})


class GeminiModel:
    """Real Gemini text generation via Vertex (needs GCP)."""

    def __init__(self, model: str = "gemini-3.5-flash"):
        self.model = model

    def generate(self, prompt: str) -> str:  # pragma: no cover - needs GCP
        from google import genai

        client = genai.Client(vertexai=True)
        resp = client.models.generate_content(model=self.model, contents=prompt)
        return resp.text
