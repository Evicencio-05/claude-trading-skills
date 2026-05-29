# MCP + Cursor Compatibility

> Short reference. Full Robinhood setup: [robinhood-mcp-integration.md](robinhood-mcp-integration.md).

## Robinhood in Cursor

- **Connect:** direct `url` → `https://agent.robinhood.com/mcp/trading` (written by `bash scripts/setup_robinhood_mcp.sh`)
- **Data for agents:** `uv run python3 scripts/robinhood_mcp.py` (not in-chat MCP tools)

Do **not** put `bash scripts/run_robinhood_mcp_stdio.sh` in `.cursor/mcp.json` — it causes `-32001` connect timeouts.

## Errors

| Code | Meaning | Action |
|------|---------|--------|
| `-32001` | Connect timeout | Use URL config from setup; restart Cursor |
| `-32600` | structuredContent | Use CLI, not CallMcpTool |

## Adding other MCP servers

1. Try direct `url` in `.cursor/mcp.json` first.
2. If tool calls fail with `-32600`, use [`scripts/mcp_stdio_structured_content_proxy.py`](../../scripts/mcp_stdio_structured_content_proxy.py) only in **terminal/CLI** subprocesses, not Cursor spawn.
3. Pin deps in `package.json` — avoid `npx -y` on every IDE start.
