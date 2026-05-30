"""FastAPI backend: read-APIs over the store + agent-triggered actions.

The agent-backed operations (process, search) are injected so the HTTP layer is
testable without a live agent or live MCP servers.
"""
