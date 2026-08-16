---
name: ta-confluence
description: >-
  Fuse TradeWhisperer candle lists (HTF stacks), Skylit GEX/VEX maps, and
  operator charts into a PLAY/WATCH/NO_TRADE setup brief with judgment coaching.
  Use for ta-confluence, candle-first or map-first screening, or when combining
  the three TA sources.
---

# TA Confluence

Follow [commands/ta-confluence.md](../../../commands/ta-confluence.md).

## Quick start

| Mode | Invoke |
|------|--------|
| Candle-first | Paste TW **list**(s) → `ta-confluence candle_first daily bias: long` |
| Map-first | Paste GEX/VEX → resolve TW via list stack → operator chart |

Always finish with **operator chart** before PLAY. Period **list** color required for PLAY (chart alone insufficient).

## Load during run

| File | When |
|------|------|
| [references/confluence_rubric.md](references/confluence_rubric.md) | Scoring + hard stops |
| [references/judgment_prompts.md](references/judgment_prompts.md) | Devil’s advocate / invalidation / process grade |
| [references/prediction_log_v15.md](references/prediction_log_v15.md) | After session — prediction / process log |
| TW / GEX / operator contracts | Via those skills — do not re-extract from scratch |

## Upstream intake (reuse)

- `tradewhisperer-charts` (lists preferred; charts optional)
- `gex-vex-maps`
- `operator-charts`
- `scripts/tw_list_resolve.py` — shortlist + `tw_stack` / `htf_fight`

## Output

- `reports/charts/confluence/session_confluence_{period}_{as_of}.{md,json}`
- `reports/charts/confluence/{TICKER}_confluence_{as_of}.{md,json}` (charted finalists)
- `reports/charts/confluence/prediction_log_{as_of}.{md,json}` (v1.5 — after real sessions)

Artifact key: `ta_confluence`. Include `tw_color`, `tw_stack`, `htf`, `artifacts.tw_lists`.

## Guardrails

- Co-pilot only — no MCP orders
- No Patreon/Skylit scrape; user-supplied artifacts only
- **Lists are TW color SoT** — list wins over chart-inferred color
- No auto `thesis_store` writes in v1
- NO_TRADE is a valid success
