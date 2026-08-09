---
name: ta-confluence
description: >-
  Fuse TradeWhisperer candles, Skylit GEX/VEX maps, and operator charts into a
  PLAY/WATCH/NO_TRADE setup brief with judgment coaching. Use for ta-confluence,
  candle-first or map-first screening, or when combining the three TA sources.
---

# TA Confluence

Follow [commands/ta-confluence.md](../../../commands/ta-confluence.md).

## Quick start

| Mode | Invoke |
|------|--------|
| Candle-first | Paste TW list → `ta-confluence candle_first daily bias: long` |
| Map-first | Paste GEX/VEX → `ta-confluence map_first` → TW color → operator chart |

Always finish with **operator chart** before PLAY.

## Load during run

| File | When |
|------|------|
| [references/confluence_rubric.md](references/confluence_rubric.md) | Scoring + hard stops |
| [references/judgment_prompts.md](references/judgment_prompts.md) | Devil’s advocate / invalidation / process grade |
| TW / GEX / operator contracts | Via those skills — do not re-extract from scratch |

## Upstream intake (reuse)

- `tradewhisperer-charts`
- `gex-vex-maps`
- `operator-charts`

## Output

- `reports/charts/confluence/session_confluence_{period}_{as_of}.{md,json}`
- `reports/charts/confluence/{TICKER}_confluence_{as_of}.{md,json}` (charted finalists)

Artifact key: `ta_confluence`.

## Guardrails

- Co-pilot only — no MCP orders
- No Patreon/Skylit scrape; user-supplied artifacts only
- No auto `thesis_store` writes in v1
- NO_TRADE is a valid success
