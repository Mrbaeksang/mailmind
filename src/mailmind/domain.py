"""Core domain types shared across MailMind.

Kept dependency-free so every other module can import them without pulling I/O.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Category(str, Enum):
    """The four triage buckets an email is classified into."""

    URGENT = "urgent"
    ACTION = "action"
    NEWSLETTER = "newsletter"
    SPAM = "spam"


@dataclass(frozen=True)
class Email:
    """A single email message, normalized from a provider's raw form."""

    id: str
    thread_id: str
    sender: str
    recipients: list[str]
    subject: str
    body: str
    date: str | None = None


@dataclass(frozen=True)
class Thread:
    """An ordered group of messages sharing a thread id."""

    id: str
    messages: list[Email] = field(default_factory=list)


@dataclass(frozen=True)
class Classification:
    """Result of classifying one email."""

    category: Category
    confidence: float


@dataclass(frozen=True)
class ThreadInsight:
    """Summary + extracted to-dos for a thread."""

    summary: list[str]
    todos: list[str]
