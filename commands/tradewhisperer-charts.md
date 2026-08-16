---
description: "Ingest TradeWhisperer Patreon candle-color lists (primary) and optional smart-candle charts into dated markdown+JSON artifacts."
argument-hint: "[list|TICKER] [daily|weekly|monthly|1D|1W|1M]"
---

# /tradewhisperer-charts

Ingest **user-supplied** TradeWhisperer inputs. **Lists are the candle-color source of truth.** Charts are optional (structure only). No news/FMP/Patreon scrape. Co-pilot only.

**Paths:** `reports/charts/tradewhisperer/` — lists `list_tw_{period}_{as_of}` · charts `{TICKER}_tw_{1D|1W|1M}_{as_of}`.

**Resolver:** after lists are on disk, HTF stacks via `uv run python3 scripts/tw_list_resolve.py stack TICKER --as-of YYYY-MM-DD` (uses latest weekly/monthly list on or before that date).

**Overlap + sector:** after list persist, `uv run python3 scripts/tw_list_resolve.py overlap --as-of YYYY-MM-DD --bias either --write-pending` → `overlap_tw_{as_of}.{md,json}` using [`config/tw_sector_map.yaml`](../config/tw_sector_map.yaml).

## PHASE 0 — INTAKE

Prefer **list** when the paste is a Patreon candle color list (or both list + chart). Classify list vs chart.

Load [input_contract.md](../.cursor/skills/tradewhisperer-charts/references/input_contract.md) + [smart_candle_colors.md](../.cursor/skills/tradewhisperer-charts/references/smart_candle_colors.md).

For lists: require `period` from title (`daily` / `weekly` / `monthly`). Prefer pasting **text** over screenshots to avoid OCR errors.

## PHASE 1 — EXTRACT

Fill envelope per contract; normalize candle colors (`BLUE-GREEN` → `BLUE_GREEN`, etc.).

**Lists — required:** `buckets` + `ticker_index` (build index from buckets if missing). Include `bullish_pct` / `bearish_pct` when present.

**Charts — optional:** structure fields (OHLC, MAs, VP, oscillators). Do **not** override a same-day list color for the ticker; if chart color disagrees with list, list wins and note chart color under `gaps`.

## PHASE 2 — PERSIST

Write `.json` + `.md`. No trade plan. No merge with other TA sources.

Confirm path in chat. For multi-period HTF, ingest each list separately (`list_tw_daily_*`, `list_tw_weekly_*`, `list_tw_monthly_*`).

## PHASE 3 — OVERLAP + SECTOR

After the session period list is on disk (and weekly/monthly exist or already on disk for lookback):

1. Run:
   ```bash
   uv run python3 scripts/tw_list_resolve.py overlap --as-of {as_of} --bias either --write-pending
   ```
2. Summarize in chat: top bull/bear overlaps and vs-benchmark rows (e.g. CVX/XOM vs XLE).
3. Report `unmapped` / `pending_added` count. Promote `pending:` → `tickers:` in `config/tw_sector_map.yaml` when the operator assigns a real benchmark (no FMP/news lookup).
4. Artifacts: `reports/charts/tradewhisperer/overlap_tw_{as_of}.{md,json}`.
