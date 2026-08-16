# Robinhood Agentic MCP + Cursor Integration

> **Read this when:** connecting Robinhood, portfolio review, or logging positions.

Official docs: [Robinhood Agentic Trading overview](https://robinhood.com/us/en/support/articles/agentic-trading-overview/)

---

## Architecture (hybrid)

| Layer | Tool | Use |
|-------|------|-----|
| **Cursor connect** | Direct `url` in `.cursor/mcp.json` | Fast OAuth, tools listed in UI |
| **Agent data (primary)** | `scripts/robinhood_mcp.py` | Accounts, positions, ingest — reliable |
| **Scheduled taxable** | `scripts/robinhood_sync.py` | Portfolio A via robin_stocks |
| **Account map** | `config/robinhood_accounts.yaml` | Single source for thesis_store keys |

In-chat MCP **tool calls** may fail with `-32600` (structuredContent). **Use the CLI** for agent workflows.

---

## Phase 0 — One-time setup

```bash
bash scripts/setup_robinhood_mcp.sh
```

- Installs local `mcp-remote` (`node_modules/`)
- Writes `.cursor/mcp.json` with **direct URL** (avoids Cursor `-32001` spawn timeout)
- Preflights `robinhood_mcp.py accounts`

First-time OAuth if `~/.mcp-auth` is empty:

```bash
./node_modules/.bin/mcp-remote-client https://agent.robinhood.com/mcp/trading
```

Restart Cursor → **Tools & MCP** → `robinhood-trading` green.

---

## CLI reference

```bash
uv run python3 scripts/robinhood_mcp.py accounts
uv run python3 scripts/robinhood_mcp.py positions --all
uv run python3 scripts/robinhood_mcp.py portfolio --account 487509309
uv run python3 scripts/robinhood_mcp.py ingest-pending
uv run python3 scripts/robinhood_mcp.py ingest-pending --dry-run
```

---

## Account map

| Portfolio | `thesis_store` | account_number (last 4) | In scope |
|-----------|----------------|-------------------------|----------|
| A taxable | `robinhood_taxable` | ••••9309 | Sync + log |
| B Roth IRA | `ira_robinhood` | ••••3854 | Discover only — **do not log** |
| C Agentic | `robinhood_agentic` | ••••7016 | Trade + log |

Full config: [config/robinhood_accounts.yaml](../../config/robinhood_accounts.yaml)

---

## Workflows

### Portfolio review

Skill: **robinhood-portfolio-review** — run CLI commands above, write `reports/portfolio/portfolio_review_YYYY-MM-DD.md` with **A + C focus** (IRA awareness only).

### Log positions (A + C only)

| Source | Command |
|--------|---------|
| A — Sync | `uv run python3 scripts/robinhood_sync.py` |
| B — MCP CLI | `uv run python3 scripts/robinhood_mcp.py ingest-pending` (filter out IRA) |

Then **log-positions** skill / [commands/log-positions.md](../../commands/log-positions.md). **Skip IRA four-questions.**

### Scripts (not MCP)

| Job | Tool |
|-----|------|
| Daily market | `scripts/pre_market.py` |
| Taxable timer | `robinhood-sync.timer` |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `-32001` timeout in Cursor | Use direct `url` config from setup (do not use wrapper in `.cursor/mcp.json`) |
| `-32600` in chat tool calls | Use `robinhood_mcp.py` CLI instead |
| CLI fails | Re-run OAuth + `bash scripts/setup_robinhood_mcp.sh` |
| `npx`/npm errors | `npm install` in repo root |

See [mcp-cursor-compat.md](mcp-cursor-compat.md) for Cursor-specific notes.

---

## Related

- [AGENTS.md](../../AGENTS.md)
- [playbook.md](../playbook.md) — A+C scope; IRA logging discontinued
- [decisions.md](../../decisions.md)
