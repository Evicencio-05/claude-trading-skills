---
name: tradewhisperer-charts
description: >-
  Ingest TradeWhisperer Patreon candle-color lists (primary) and optional
  smart-candle charts into dated artifacts. Use when the user pastes TW lists,
  daily/weekly/monthly color lists, TradingView charts, says tradewhisperer-charts,
  or provides TradexWhisperer overlays.
---

# TradeWhisperer Charts

Follow [commands/tradewhisperer-charts.md](../../../commands/tradewhisperer-charts.md).

## Load during extract

| File | When |
|------|------|
| [references/input_contract.md](references/input_contract.md) | Always |
| [references/smart_candle_colors.md](references/smart_candle_colors.md) | Always for color mapping |

## Output

| Kind | Files |
|------|-------|
| List (preferred) | `list_tw_{daily\|weekly\|monthly}_{YYYY-MM-DD}.{md,json}` |
| Overlap + sector | `overlap_tw_{YYYY-MM-DD}.{md,json}` |
| Chart (optional) | `{TICKER}_tw_{1D\|1W\|1M}_{YYYY-MM-DD}.{md,json}` |

Artifact key: `tradewhisperer_charts`.

HTF stack helper: `uv run python3 scripts/tw_list_resolve.py stack TICKER --as-of YYYY-MM-DD`.

Overlap + sector (after list persist): `uv run python3 scripts/tw_list_resolve.py overlap --as-of YYYY-MM-DD --bias either --write-pending` — map: `config/tw_sector_map.yaml`. Overlap artifacts include a **Pre-start watch** (W+M aligned, daily not started).

## Guardrails

- **Lists are candle-color source of truth** — prefer list over chart-inferred color
- User-supplied only — no WebSearch, news, FMP, or Patreon scrape
- Co-pilot only — no MCP orders
- Do not invent candle meanings beyond [smart_candle_colors.md](references/smart_candle_colors.md)
- Do not invent sector mappings — unmapped tickers go to `pending:` for operator fill
