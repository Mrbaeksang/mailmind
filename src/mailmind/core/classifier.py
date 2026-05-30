"""Classify an email into a triage Category using a text model.

The deterministic, testable parts are prompt construction and response parsing;
the model call itself goes through the TextModel port.
"""

from __future__ import annotations

from mailmind.core._json import extract_json_object
from mailmind.domain import Category, Classification, Email
from mailmind.ports import TextModel

_CATEGORIES = ", ".join(c.value for c in Category)


def build_prompt(email: Email) -> str:
    return (
        "Classify the email into exactly one category: "
        f"{_CATEGORIES}.\n"
        'Respond with JSON: {"category": <one of the categories>, '
        '"confidence": <0..1>}.\n\n'
        f"From: {email.sender}\n"
        f"Subject: {email.subject}\n\n"
        f"{email.body}"
    )


def parse_classification(text: str) -> Classification:
    """Parse the model response, tolerating markdown fences and surrounding prose.

    Falls back to ACTION with zero confidence on anything unparseable, so a bad
    response surfaces as "needs a human" rather than crashing the pipeline.
    """
    data = extract_json_object(text)
    if data is not None:
        try:
            return Classification(
                category=Category(str(data["category"]).strip().lower()),
                confidence=float(data["confidence"]),
            )
        except (ValueError, KeyError, TypeError):
            pass
    return Classification(category=Category.ACTION, confidence=0.0)


def classify(email: Email, model: TextModel) -> Classification:
    response = model.generate(build_prompt(email))
    return parse_classification(response)
