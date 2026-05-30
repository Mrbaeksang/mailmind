"""Safety/config invariants for the official MCP integrations."""

from mailmind.mcp.config import (
    KNOWN_GMAIL_TOOLS,
    gmail_allowed_tools,
    mongo_disabled_tools,
)


def test_no_send_capable_gmail_tool_is_allowed():
    # The hard safety rule: the agent can never send mail.
    assert not any("send" in tool.lower() for tool in gmail_allowed_tools())


def test_gmail_allowed_tools_are_real_official_tools():
    assert set(gmail_allowed_tools()) <= set(KNOWN_GMAIL_TOOLS)


def test_gmail_allowed_tools_cover_the_features_we_need():
    allowed = set(gmail_allowed_tools())
    assert {"create_draft", "get_thread", "search_threads", "label_message"} <= allowed


def test_mongo_disabled_tools_block_destructive_operations():
    disabled = set(mongo_disabled_tools())
    assert {"drop-database", "drop-collection", "delete-many"} <= disabled
