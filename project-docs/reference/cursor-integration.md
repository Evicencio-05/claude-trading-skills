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

## Portfolio MCP in Cursor

**Default:** Use Claude Code for `portfolio-manager` with Alpaca MCP ([alpaca-mcp-setup.md](../../skills/portfolio-manager/references/alpaca-mcp-setup.md)).

**Cursor option:** Add the same MCP server in Cursor → Settings → MCP (project or user config). Tool names must match what `portfolio-manager` expects (`get_account_info`, `get_positions`, …). Use paper trading keys until validated.

**Without MCP:** Robinhood path — `scripts/robinhood_sync.py` then `commands/log-positions.md`.

## Do not

- Copy skill trees into `.cursor/skills/` (breaks single source of truth)
- Run `pre_market.py` via Cursor Agent on a schedule (use systemd/cron)
- Commit `.env`, `.mcp.json`, or API keys

## Adding skills to Cursor

```bash
ln -sfn ../../skills/<skill-name> .cursor/skills/<skill-name>
```

Document new symlinks in `.cursor/skills/README.md` if part of the daily stack.
