---
name: options-flow-tail
description: >-
  Rank options flow screener rows for tailing. Extract screenshot or pasted
  rows, score whale prints with veteran rubric, enrich with market context and
  research, output primary tail with lite options structure. Use when user
  pastes options flow screener, asks which flow to tail, or says
  options-flow-tail.
---

# Options Flow Tail

Follow [commands/options-flow-tail.md](../../../commands/options-flow-tail.md).

## Quick start

User pastes screener screenshot or row text → extract table → score → enrich top 2 → lite structure for primary → save report.

## Load during Phase 3

[references/tail_rubric.md](references/tail_rubric.md) — disqualifiers, weights, adjustments.

## Pipeline reuse (no auto-fetch)

| Artifact | Path |
|----------|------|
| Market posture | `reports/logs/market_context_YYYY-MM-DD.json` |
| Research | `reports/research/{TICKER}_*.md` |
| Entry watchlist | `reports/logs/entry_watchlist_YYYY-MM-DD.json` |
| Sector | `reports/market/sector/sector_rotation_YYYY-MM-DD.json` |

## Output

- `reports/flow/flow_tail_{YYYY-MM-DD}.md`
- `reports/flow/flow_tail_{YYYY-MM-DD}.json`

## Guardrails

- Co-pilot only — no MCP orders
- No Unusual Whales / QuantData API — user supplies screener data
- FMP earnings check on primary pick only
- **NO TAIL** is always valid
