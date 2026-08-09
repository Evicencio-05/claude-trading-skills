---
name: agentic-copilot-trade
description: >-
  Agentic co-pilot: draft a Portfolio C equity plan from research, size within
  dollar caps, MCP review_equity_order, and place only after the user confirms.
  Use when the user says agentic-copilot-trade, co-pilot trade, place on Agentic,
  or asks to buy on Portfolio C with confirmation gates.
---

# Agentic Co-Pilot Trade

Follow [commands/agentic-copilot-trade.md](../../../commands/agentic-copilot-trade.md).

## Load

| Resource | When |
|----------|------|
| [config/agentic_copilot.yaml](../../../config/agentic_copilot.yaml) or `.example` | Always (PASS 0) |
| [config/robinhood_accounts.yaml](../../../config/robinhood_accounts.yaml) | Resolve Agentic account |
| Latest research + market_context | PASS 1 |
| Skill `position-sizer` | PASS 2 sizing |

## Output

- Plan JSON: `reports/logs/agentic_copilot_plan_{TICKER}_{YYYY-MM-DD}.json`
- Thesis via `thesis_store.py` / `/log-positions` after place

## Guardrails

- Portfolio C (`robinhood_agentic`) only — never MCP trade IRA or taxable
- Co-pilot: no `place_equity_order` without explicit user confirm
- No autonomous execution before Phase 3B
