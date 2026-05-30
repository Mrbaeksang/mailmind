"""Static config + safety policy for the two official MCP servers.

These are pure values/functions so the safety invariants (no send tool, no
destructive DB tools) can be unit-tested without any network access.
"""

from __future__ import annotations

# Google's official Gmail MCP server (Developer Preview).
GMAIL_MCP_ENDPOINT = "https://gmailmcp.googleapis.com/mcp/v1"

# The full toolset the Gmail MCP server exposes (verified from Google's docs).
# Note: there is deliberately no send tool — sending is impossible by design.
KNOWN_GMAIL_TOOLS = (
    "create_draft",
    "list_drafts",
    "get_thread",
    "search_threads",
    "create_label",
    "list_labels",
    "label_message",
    "label_thread",
    "unlabel_message",
    "unlabel_thread",
)

# The subset the agent is allowed to call: read, search, label, and draft only.
_GMAIL_ALLOWED = (
    "create_draft",
    "list_drafts",
    "get_thread",
    "search_threads",
    "create_label",
    "list_labels",
    "label_message",
    "label_thread",
)

# Destructive MongoDB MCP tools the agent must never be able to call.
_MONGO_DISABLED = (
    "drop-database",
    "drop-collection",
    "delete-many",
    "delete-one",
    "drop-index",
    "atlas",
)


def gmail_allowed_tools() -> list[str]:
    return list(_GMAIL_ALLOWED)


def mongo_disabled_tools() -> list[str]:
    return list(_MONGO_DISABLED)
