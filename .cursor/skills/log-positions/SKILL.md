---
name: log-positions
description: >-
  Log Robinhood Portfolio A (taxable) and C (Agentic) positions to
  trader-memory-core with four thesis questions. Skip IRA (B). Use after
  robinhood_sync.py, after MCP Agentic/taxable fetch, or when the user asks
  to log positions for A/C.
---

# Log Positions

Follow [commands/log-positions.md](../../../commands/log-positions.md).

## Choose source

| Source | Prerequisite |
|--------|----------------|
| **A — Sync** | `uv run python3 scripts/robinhood_sync.py` then read `state/pending_ingest.json` |
| **B — MCP CLI** | `uv run python3 scripts/robinhood_mcp.py ingest-pending` (then read `pending_ingest.json`) |

Account mapping: [decisions.md](../../../decisions.md) discovery table.

## MCP guardrails

- Read-only unless user explicitly requests a trade (Phase 3B+ co-pilot confirm).
- Log **Portfolio A + C only** — skip `ira_robinhood` / IRA four-questions.
- Register via thesis-manager or `thesis_store.register()` — not `thesis_ingest.py`.

See [robinhood-mcp-integration.md](../../../project-docs/reference/robinhood-mcp-integration.md).
