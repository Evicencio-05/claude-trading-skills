# Operator Charts — Input Contract

> **Status:** Active (operator brief 2026-08-09). Four primary indicators only. VP shelves: [luxalgo_vp_shelves.md](luxalgo_vp_shelves.md) · [TradingView script](https://www.tradingview.com/v/zVCsx5DL/).

Operator pastes their own TradingView chart screenshots. Distinct from TradeWhisperer and upstream `technical-analyst`.

Artifact stem: `{TICKER}_operator_{as_of}` → `reports/charts/operator/`.

---

## Four indicators (extract all that are visible)

| # | Indicator | How it appears | Extract into |
|---|-----------|----------------|--------------|
| 1 | **Support / Resistance** | Thin **white** horizontal lines | `sr_levels` |
| 2 | **Fibonacci extensions** | Colorful horizontal lines with ratio labels (0, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, …) | `fib_levels` |
| 3 | **VP shelves** | LuxAlgo Volume Profile with Node Detection — orange/blue/gray histogram on right (sometimes extends left); peak/trough/HVN shelves | `vp` |
| 4 | **SMAs** | **Orange = 50**, **Blue = 100**, **Green = 200** | `sma` |

Optional visible extras (record if labeled, do not invent): volume pane, RSI, earnings markers (`E`), major thick historical levels (if distinct from white S/R).

---

## Extract fields (`extracted` object)

| Field | Type | Notes |
|-------|------|-------|
| `category` | `"operator"` | |
| `timeframe` | `"1D"` \| `"1W"` \| … | Chart header |
| `last` | number \| null | |
| `change` / `change_pct` | number \| null | If shown |
| `volume` | string \| null | Session volume if labeled |
| `sma` | object | `{ "50": number\|null, "100": number\|null, "200": number\|null }` — map by color |
| `price_vs_sma` | object \| null | e.g. `{ "50": "above\|below\|at", "100": "...", "200": "..." }` |
| `sr_levels` | number[] | White horizontal S/R — all readable prices |
| `fib_levels` | object[] | `{ "ratio": "0.786", "price": 93.85, "color": "yellow" }` |
| `vp` | object | See VP subsection |
| `major_levels` | number[] \| null | Thick historical lines if distinct from white S/R |
| `rsi` | number \| null | If RSI pane labeled |
| `earnings_markers` | string \| null | Past/future `E` notes if relevant |
| `structure_notes` | string \| null | Short TA note from levels only (no news) |
| `chart_timestamp` | string \| null | |

### `vp` object

| Field | Type | Notes |
|-------|------|-------|
| `indicator` | `"luxalgo_vp_node_detection"` | |
| `lookback_note` | string \| null | If profile range obvious |
| `poc` | number \| null | Point of Control if labeled |
| `vah` / `val` | number \| null | Value area high/low if labeled |
| `peak_nodes` | number[] | Peak volume node prices / shelves |
| `trough_nodes` | number[] | Low-volume nodes if marked |
| `highest_volume_zones` | string[] | e.g. `"75–115 shelf"` |
| `lowest_volume_zones` | string[] | Rejection / LVN bands |
| `profile_labels` | object \| null | Any numeric labels on VP (high/low/nodes) |
| `colors_note` | string \| null | Orange/blue = value-area / up-down customization; gray = lower volume |

---

## Reading rules

1. SMA colors are fixed: orange→50, blue→100, green→200. Do not rename.
2. White lines = operator S/R; extract every readable level near price first, then distant.
3. Fib: prefer labeled ratios; if label unreadable, store price with `ratio: null`.
4. VP shelves: load [luxalgo_vp_shelves.md](luxalgo_vp_shelves.md). Peaks = consolidation / acceptance; troughs / lowest volume = rejection / thin interest; highest volume = strong acceptance.
5. Structure notes may relate price to 50/100/200 and nearest fib/S/R/VP shelf — **no news, no fundamentals**.
6. Do not invent levels not visible on the screenshot.

---

## Shared JSON envelope

```json
{
  "source": "operator",
  "ticker": "HOOD",
  "as_of": "2026-08-08",
  "inputs": [{"type": "image", "note": "operator 1D chart"}],
  "extracted": { "category": "operator", "...": "..." },
  "confidence": "high|medium|low",
  "gaps": [],
  "next": null
}
```

---

## Out of scope

- WebSearch / news / FMP
- TradeWhisperer candle colors or Skylit GEX/VEX (other skills)
- Auto-merging with `technical-analyst` unless contract later says so
- Trade plans / MCP orders
