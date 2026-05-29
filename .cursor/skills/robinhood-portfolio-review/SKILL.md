---
name: robinhood-portfolio-review
description: >-
  Review all Robinhood accounts via official Agentic MCP. Fetches positions and
  balances, flags IRA options eligibility, cross-checks trader-memory-core, and
  writes a dated report to reports/. Use when the user asks for portfolio review,
  Robinhood positions, account summary, or MCP portfolio snapshot.
---

# Robinhood Portfolio Review

Requires `bash scripts/setup_robinhood_mcp.sh` once (CLI + optional Cursor URL).

## Before starting

1. Read IRA rules in [project-docs/playbook.md](../../../project-docs/playbook.md) (Portfolio B section).
2. Run broker CLI (primary — works even when in-chat MCP calls fail):

```bash
uv run python3 scripts/robinhood_mcp.py accounts
uv run python3 scripts/robinhood_mcp.py positions --all
```

## Workflow

### 1. Fetch via CLI

Use `scripts/robinhood_mcp.py` to retrieve (not in-chat MCP tools):

- All accounts (name, account number/id, buying power, equity)
- Open positions per account (stocks and options: ticker, qty, avg cost, market value, P&L)
- For options: strike, expiry, type, contracts

Do not place orders unless the user explicitly requests a trade (Phase 5+ only).

### 2. Cross-check theses

```bash
uv run python3 skills/trader-memory-core/scripts/thesis_store.py \
  --state-dir state/theses/ list
```

Note positions in MCP but **not** in thesis store (untracked).

### 3. Write report

Save to `reports/portfolio_review_YYYY-MM-DD.md` with:

```markdown
# Portfolio Review — YYYY-MM-DD
**Source:** Robinhood Agentic MCP (read-only)

## Account summary
(table per account)

## Positions by account
### robinhood_taxable / ira_robinhood / robinhood_agentic
(per position: ticker, size, cost, value, thesis_id if known)

## Options — IRA eligibility (Portfolio B only)
| Ticker | Strategy | IRA-eligible |
|--------|----------|--------------|

## Untracked vs trader-memory-core
(list MCP positions missing from thesis store)

## Notes
(risks, concentration, upcoming expiries)
```

### 4. IRA enforcement

For `ira_robinhood` options, flag **IRA-eligible: Yes/No** before any actionable suggestion.
Non-eligible strategies are educational only.

## References

- [robinhood-mcp-integration.md](../../../project-docs/reference/robinhood-mcp-integration.md)
- [decisions.md](../../../decisions.md) — account map
