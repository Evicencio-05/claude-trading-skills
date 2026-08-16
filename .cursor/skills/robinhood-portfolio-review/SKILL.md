---
name: robinhood-portfolio-review
description: >-
  Review Robinhood accounts via official Agentic MCP with emphasis on Portfolio
  A (taxable) and C (Agentic). Fetches positions and balances, cross-checks
  trader-memory-core for A+C, and writes a dated report to reports/. Skip IRA
  (B) thesis logging. Use when the user asks for portfolio review, Robinhood
  positions, account summary, or MCP portfolio snapshot.
---

# Robinhood Portfolio Review

Requires `bash scripts/setup_robinhood_mcp.sh` once (CLI + optional Cursor URL).

## Before starting

1. Account scope: **A + C in focus** — IRA (B) may appear in MCP lists but is **not logged** ([playbook.md](../../../project-docs/playbook.md)).
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

Do not place orders unless the user explicitly confirms an Agentic (C) co-pilot plan.

### 2. Cross-check theses (A + C)

```bash
uv run python3 skills/trader-memory-core/scripts/thesis_store.py \
  --state-dir state/theses/ list
```

Note **A/C** positions in MCP but **not** in thesis store (untracked). Do not queue IRA four-questions.

### 3. Write report

Save to `reports/portfolio/portfolio_review_YYYY-MM-DD.md` with:

```markdown
# Portfolio Review — YYYY-MM-DD
**Source:** Robinhood Agentic MCP (read-only)
**Focus:** Portfolio A (taxable) + C (Agentic). IRA listed for awareness only — not logged.

## Account summary
(table per account — highlight A and C)

## Positions by account
### robinhood_taxable
### robinhood_agentic
### ira_robinhood (awareness only — do not log)
(per position: ticker, size, cost, value, thesis_id if known for A/C)

## Untracked vs trader-memory-core (A + C)
(list MCP A/C positions missing from thesis store)

## Notes
(risks, concentration, upcoming expiries on A/C)
```

### 4. Logging follow-up

If A/C positions need theses: `/log-positions` — **skip `ira_robinhood`**.

## References

- [robinhood-mcp-integration.md](../../../project-docs/reference/robinhood-mcp-integration.md)
- [decisions.md](../../../decisions.md) — account map
