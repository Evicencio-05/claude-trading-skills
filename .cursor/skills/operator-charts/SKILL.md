---
name: operator-charts
description: >-
  Ingest the operator's own TradingView charts (S/R, Fibonacci extensions,
  LuxAlgo VP shelves, 50/100/200 SMA) into a dated artifact. Use when the user
  pastes their charting, says operator-charts, or provides personal TA markups.
---

# Operator Charts

Follow [commands/operator-charts.md](../../../commands/operator-charts.md).

## Quick start

User pastes their chart → extract four indicators → save under `reports/charts/operator/`.

## Load during extract

| File | When |
|------|------|
| [references/input_contract.md](references/input_contract.md) | Always |
| [references/luxalgo_vp_shelves.md](references/luxalgo_vp_shelves.md) | When VP shelves visible |

Optional later: upstream `skills/technical-analyst/references/technical_analysis_framework.md` — only if contract says so.

## Output

- `reports/charts/operator/{TICKER}_operator_{YYYY-MM-DD}.md`
- `reports/charts/operator/{TICKER}_operator_{YYYY-MM-DD}.json`

Artifact key: `operator_charts`.

## Guardrails

- User-supplied only — no WebSearch, news, or FMP
- Co-pilot only — no MCP orders
- Do not merge with TradeWhisperer or GEX/VEX in this skill
- SMA colors fixed: orange 50 / blue 100 / green 200
