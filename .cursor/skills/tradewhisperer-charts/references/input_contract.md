# TradeWhisperer — Input Contract

> **Status:** Active. Two categories: **charts** and **lists**. Color lexicon: [smart_candle_colors.md](smart_candle_colors.md).

| Category | What operator pastes | Artifact stem |
|----------|----------------------|---------------|
| **Charts** | TradingView `@TradexWhisperer` smart-candle chart (1D / 1W / 1M) | `{TICKER}_tw_{1D\|1W\|1M}_{as_of}` |
| **Lists** | Patreon candle color list + bullish/bearish % | `list_tw_{daily\|weekly\|monthly}_{as_of}` |

Output: `reports/charts/tradewhisperer/`.

## Charts — extract

`category`, `timeframe`, `last`, `change`/`change_pct`, `ohlc`, `volume`, `current_candle_color`, `recent_candle_sequence`, `ma_levels`, `volume_profile_notes`, `oscillators`, `price_vs_mas`, `chart_timestamp`.

Normalize colors via lexicon. HTF dominates. No news/DD fetch.

## Lists — extract

`category: list`, `period`, `as_of_list`, `bullish_pct`, `bearish_pct`, `buckets` (BLUE, BLUE_GREEN, GREEN, PINK, PINK_RED, RED, TRIM_OPTION), `ticker_index`, `trim_option`. JSON `ticker` = `MARKET`.

## Envelope

`source: tradewhisperer`, `inputs`, `extracted`, `confidence`, `gaps`, `next`.
