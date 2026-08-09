---
description: "Ingest TradeWhisperer smart-candle charts and Patreon candle-color lists into dated markdown+JSON artifacts."
argument-hint: "[TICKER|list] [1D|1W|1M|daily|weekly|monthly]"
---

# /tradewhisperer-charts

Ingest **user-supplied** TradeWhisperer **charts** and/or **lists**. No news/FMP/Patreon scrape. Co-pilot only.

**Paths:** `reports/charts/tradewhisperer/` — charts `{TICKER}_tw_{1D|1W|1M}_{as_of}` · lists `list_tw_{period}_{as_of}`.

## PHASE 0 — INTAKE

Classify chart vs list. Load [input_contract.md](../.cursor/skills/tradewhisperer-charts/references/input_contract.md) + [smart_candle_colors.md](../.cursor/skills/tradewhisperer-charts/references/smart_candle_colors.md).

## PHASE 1 — EXTRACT

Fill envelope per contract; normalize candle colors.

## PHASE 2 — PERSIST

Write `.json` + `.md`. No trade plan. No merge with other TA sources.
