#!/usr/bin/env bash
# Robinhood MCP stdio stack for Cursor: structuredContent proxy + local mcp-remote.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

MCP_REMOTE="${ROOT}/node_modules/.bin/mcp-remote"
if [[ ! -x "$MCP_REMOTE" ]]; then
  echo "mcp-remote not installed. Run: bash scripts/setup_robinhood_mcp.sh" >&2
  exit 1
fi

exec python3 scripts/mcp_stdio_structured_content_proxy.py -- \
  "$MCP_REMOTE" \
  "https://agent.robinhood.com/mcp/trading" \
  --transport http-only \
  --auth-timeout 120 \
  --silent
