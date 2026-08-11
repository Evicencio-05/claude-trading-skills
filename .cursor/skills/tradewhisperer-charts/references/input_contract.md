# TradeWhisperer — Input Contract

> **Status:** Active. **List-first:** Patreon candle color lists are the color source of truth. Charts are optional for structure. Color lexicon: [smart_candle_colors.md](smart_candle_colors.md).

| Category | What operator pastes | Artifact stem | Role |
|----------|----------------------|---------------|------|
| **Lists** (preferred) | Patreon candle color list + bullish/bearish % | `list_tw_{daily\|weekly\|monthly}_{as_of}` | Color SoT + HTF stacks |
| **Charts** (optional) | TradingView `@TradexWhisperer` smart-candle chart (1D / 1W / 1M) | `{TICKER}_tw_{1D\|1W\|1M}_{as_of}` | Structure only (MAs, VP, oscillators) |

Output: `reports/charts/tradewhisperer/`.

## List-first rules

1. Prefer pasting list **text** over screenshots (fewer OCR misreads).
2. Always set `period` from the list title: `daily` | `weekly` | `monthly`.
3. Always write **`buckets`** and **`ticker_index`** (build index from buckets if missing).
4. Normalize bucket keys: `BLUE-GREEN` → `BLUE_GREEN`, `PINK-RED` → `PINK_RED`, `TRIM-OPTION` → `TRIM_OPTION`.
5. **Conflict rule:** if list color and chart-inferred color disagree for the same ticker/period, **list wins**; note chart color under `gaps`.
6. HTF overlap: ingest separate list files per period; resolve with `scripts/tw_list_resolve.py`.

## Lists — extract

`category: list`, `period`, `as_of_list`, `bullish_pct`, `bearish_pct`, `buckets` (BLUE, BLUE_GREEN, GREEN, PINK, PINK_RED, RED, TRIM_OPTION), `ticker_index`, `trim_option`. JSON `ticker` = `MARKET`.

### `ticker_index` (required)

Map every ticker in any bucket to its normalized color:

```json
"ticker_index": {"CVX": "BLUE", "AMSC": "PINK", "AAOI": "GREEN"}
```

### Example envelope (list)

```json
{
  "source": "tradewhisperer",
  "ticker": "MARKET",
  "as_of": "2026-08-10",
  "extracted": {
    "category": "list",
    "period": "daily",
    "as_of_list": "2026-08-10",
    "bullish_pct": 68.44,
    "bearish_pct": 31.56,
    "buckets": {
      "BLUE": ["CVX", "XOM"],
      "PINK": ["AMSC"],
      "GREEN": ["AAOI"]
    },
    "ticker_index": {"CVX": "BLUE", "XOM": "BLUE", "AMSC": "PINK", "AAOI": "GREEN"}
  }
}
```

## Charts — extract

`category`, `timeframe`, `last`, `change`/`change_pct`, `ohlc`, `volume`, `current_candle_color`, `recent_candle_sequence`, `ma_levels`, `volume_profile_notes`, `oscillators`, `price_vs_mas`, `chart_timestamp`.

Normalize colors via lexicon. Do not use chart color to override a same-period list. HTF dominates via **lists** when present. No news/DD fetch.

## Envelope

`source: tradewhisperer`, `inputs`, `extracted`, `confidence`, `gaps`, `next`.
