#!/usr/bin/env bash
# Robinhood MCP setup: local mcp-remote + CLI preflight + Cursor config (direct URL).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

MCP_JSON="${ROOT}/.cursor/mcp.json"
MCP_REMOTE_BIN="${ROOT}/node_modules/.bin/mcp-remote"
MCP_REMOTE_CLIENT="${ROOT}/node_modules/.bin/mcp-remote-client"
RH_URL="https://agent.robinhood.com/mcp/trading"
CLI_TIMEOUT="${CLI_TIMEOUT:-35}"

info() { echo "==> $*"; }
warn() { echo "WARNING: $*" >&2; }

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

write_mcp_json_url() {
  mkdir -p "${ROOT}/.cursor"
  cat >"$MCP_JSON" <<'EOF'
{
  "mcpServers": {
    "robinhood-trading": {
      "url": "https://agent.robinhood.com/mcp/trading"
    }
  }
}
EOF
}

install_deps() {
  require_cmd npm
  require_cmd node
  require_cmd python3
  info "Installing mcp-remote (local node_modules)..."
  npm install --no-fund --no-audit
  if [[ ! -x "$MCP_REMOTE_BIN" ]]; then
    echo "mcp-remote binary missing after npm install" >&2
    exit 1
  fi
}

maybe_preauth() {
  local auth_dir="${MCP_REMOTE_CONFIG_DIR:-${HOME}/.mcp-auth}"
  if [[ -d "$auth_dir" ]] && [[ -n "$(ls -A "$auth_dir" 2>/dev/null || true)" ]]; then
    info "Found existing MCP auth in ${auth_dir}"
    return 0
  fi
  warn "No MCP OAuth tokens found."
  echo "Run in terminal (browser OAuth), then re-run setup:"
  echo "  ${MCP_REMOTE_CLIENT} ${RH_URL}"
  if [[ -t 0 ]]; then
    read -r -p "Press Enter after OAuth completes (or Ctrl-C to exit)... " _
  else
    return 1
  fi
}

preflight_cli() {
  info "Preflight: robinhood_mcp.py accounts (timeout ${CLI_TIMEOUT}s)..."
  if timeout "$CLI_TIMEOUT" python3 scripts/robinhood_mcp.py accounts 2>/dev/null | grep -q 'robinhood_taxable'; then
    info "CLI preflight OK."
    return 0
  fi
  warn "CLI preflight failed."
  return 1
}

main() {
  install_deps
  maybe_preauth || true
  write_mcp_json_url
  info "Wrote ${MCP_JSON} (direct URL — fast Cursor connect, no spawn timeout)."

  if preflight_cli; then
    echo ""
    echo "Robinhood data plane ready."
    echo "  uv run python3 scripts/robinhood_mcp.py accounts"
    echo "  uv run python3 scripts/robinhood_mcp.py positions --all"
    echo "  uv run python3 scripts/robinhood_mcp.py ingest-pending --dry-run"
  else
    warn "CLI preflight failed — fix OAuth, then: bash scripts/setup_robinhood_mcp.sh"
  fi

  echo ""
  echo "Restart Cursor → Tools & MCP → robinhood-trading should connect (green)."
  echo "Use CLI for agent workflows; in-chat MCP tool calls may still error -32600."
}

main "$@"
