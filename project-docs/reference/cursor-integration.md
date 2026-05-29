# Cursor Integration

> **Read this when:** setting up Cursor for this repo, wiring MCP, or deciding Claude vs Cursor for a workflow.

## What lives where

| Path | Role |
|------|------|
| `skills/` | Canonical skill source (scripts + references + SKILL.md) |
| `.cursor/skills/` | Symlinks + workflow wrappers (`deep-research`, `log-positions`) |
| `.cursor/rules/` | Auto-loaded session router, Python conventions, command map |
| `commands/` | Workflow specs (shared by Claude slash commands and Cursor) |
| [AGENTS.md](../../AGENTS.md) | Hybrid routing table |

## Setup checklist

1. Open repo in Cursor — `project-router.mdc` loads automatically.
2. Confirm symlinks: `ls -la .cursor/skills/` — each entry should point to `../../skills/<name>`.
3. Optional: `ln -sfn "$(pwd)/skills/<name>" ~/.claude/skills/<name>` for Claude Code parity.
4. Ensure `.env` exists at repo root with `FMP_API_KEY` etc. (gitignored).
5. Run `uv run python3 scripts/pre_market.py --dry-run` to verify daily stack.
6. Optional: install `robinhood-sync.timer` — see [launchd/README.md](../../launchd/README.md).

## Robinhood MCP in Cursor (primary for this fork)

1. `bash scripts/setup_robinhood_mcp.sh` (writes `.cursor/mcp.json`)
2. Requires Node.js + `npm` on PATH
3. Restart Cursor; OAuth via `mcp-remote-client` on first run if prompted by setup
4. Full guide: [robinhood-mcp-integration.md](robinhood-mcp-integration.md)
5. MCP errors in Cursor: [mcp-cursor-compat.md](mcp-cursor-compat.md)

Skills: `robinhood-portfolio-review`, `log-positions`. Rule: `.cursor/rules/robinhood-mcp.mdc`.

**Hybrid:** Keep `robinhood_sync.py` timer for Portfolio A; use MCP for live reads and IRA/Agentic logging.

## Alpaca MCP (optional)

`portfolio-manager` uses Alpaca MCP — optional in Claude Code, not required for Robinhood workflows.
See [alpaca-mcp-setup.md](../../skills/portfolio-manager/references/alpaca-mcp-setup.md).

## Do not

- Copy skill trees into `.cursor/skills/` (breaks single source of truth)
- Run `pre_market.py` via Cursor Agent on a schedule (use systemd/cron)
- Commit `.env`, `.mcp.json`, or API keys

## Adding skills to Cursor

```bash
ln -sfn ../../skills/<skill-name> .cursor/skills/<skill-name>
```

Document new symlinks in `.cursor/skills/README.md` if part of the daily stack.
