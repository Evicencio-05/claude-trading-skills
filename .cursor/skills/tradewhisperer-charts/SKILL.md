---
name: tradewhisperer-charts
description: >-
  Ingest TradeWhisperer smart-candle charts and Patreon candle-color lists into
  dated artifacts. Use when the user pastes TW TradingView charts, daily/weekly/
  monthly color lists, says tradewhisperer-charts, or provides TradexWhisperer overlays.
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
| Chart | `{TICKER}_tw_{1D\|1W\|1M}_{YYYY-MM-DD}.{md,json}` |
| List | `list_tw_{daily\|weekly\|monthly}_{YYYY-MM-DD}.{md,json}` |

Artifact key: `tradewhisperer_charts`.

## Guardrails

- User-supplied only — no WebSearch, news, FMP, or Patreon scrape
- Co-pilot only — no MCP orders
- Do not invent candle meanings beyond [smart_candle_colors.md](references/smart_candle_colors.md)
