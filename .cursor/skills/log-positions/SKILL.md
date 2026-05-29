---
name: log-positions
description: >-
  Log Robinhood positions to trader-memory-core with four thesis questions per
  position. Use after robinhood_sync.py, after MCP position fetch, or when the
  user asks to log positions, register theses, or update position memory.
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

- Read-only unless user explicitly requests a trade (Phase 5+).
- IRA: eligibility flag on every options line.
- Register via thesis-manager or `thesis_store.register()` — not `thesis_ingest.py`.

See [robinhood-mcp-integration.md](../../../project-docs/reference/robinhood-mcp-integration.md).
