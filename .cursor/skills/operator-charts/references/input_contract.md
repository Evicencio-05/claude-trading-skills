# Operator Charts — Input Contract

> **Status:** Active (operator brief 2026-08-09; RSI strength rules 2026-08-09). Five primary indicators. VP shelves: [luxalgo_vp_shelves.md](luxalgo_vp_shelves.md) · [TradingView script](https://www.tradingview.com/v/zVCsx5DL/).

Operator pastes their own TradingView chart screenshots. Distinct from TradeWhisperer and upstream `technical-analyst`.

Artifact stem: `{TICKER}_operator_{as_of}` → `reports/charts/operator/`.

---

## Five indicators (extract all that are visible)

| # | Indicator | How it appears | Extract into |
|---|-----------|----------------|--------------|
| 1 | **Support / Resistance** | Thin **white** horizontal lines | `sr_levels` |
| 2 | **Fibonacci extensions** | Colorful horizontal lines with ratio labels (0, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, …); multiple fib anchors OK | `fib_levels` / `fib_sets` |
| 3 | **VP shelves** | LuxAlgo Volume Profile with Node Detection — orange/blue/gray histogram on right (sometimes extends left); peak/trough/HVN shelves | `vp` |
| 4 | **SMAs** | **Orange = 50**, **Blue = 100**, **Green = 200** | `sma` |
| 5 | **RSI (strength)** | Bottom line chart: **white** RSI vs **yellow** signal vs **50** midline | `rsi` |

Optional extras (record if labeled): volume pane, earnings markers (`E`), channel/trend lines, major thick historical levels (if distinct from white S/R).

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
| `fib_levels` | object[] | Primary/visible set: `{ "ratio": "0.786", "price": 93.85, "color": "yellow" }` |
| `fib_sets` | object[] \| null | When multiple fib anchors pasted: `{ "anchor_note", "levels": [...] }` |
| `vp` | object | See VP subsection |
| `major_levels` | number[] \| null | Thick historical lines if distinct from white S/R |
| `rsi` | object \| null | See RSI subsection (required when pane visible) |
| `channel` | object \| null | `{ "type", "status", "notes" }` if drawn |
| `earnings_markers` | string \| null | Past/future `E` notes if relevant |
| `structure_notes` | string \| null | Short TA note from levels only (no news) |
| `operator_thesis` | string \| null | Operator’s stated setup in their words |
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

### `rsi` object (operator strength rules)

| Field | Type | Notes |
|-------|------|-------|
| `white` | number \| null | White RSI line |
| `yellow` | number \| null | Yellow signal line |
| `mid_50` | `50` | Fixed reference |
| `buyer_strength` | bool \| null | White **above** yellow **and** above 50 |
| `seller_strength` | bool \| null | White **below** yellow **and** below 50 |
| `deterioration_watch` | string \| null | White trending back toward 50 from **>70** (buyers fading) or **<30** (sellers fading) |
| `hold_note` | string \| null | e.g. must hold reclaim of 50 after cross |

**Rules (operator-defined):**

1. Who has strength = white vs yellow **and** vs 50.
2. Buyers strong when white > yellow and white > 50; sellers strong when white < yellow and white < 50.
3. Strength tends to deteriorate/reverse when white trends back to 50 from a high above 70 or a low under 30.
4. After a reclaim of 50, watch that white **holds** the 50 area and does not break back below.

---

## Reading rules

1. SMA colors are fixed: orange→50, blue→100, green→200. Do not rename.
2. White lines = operator S/R; extract every readable level near price first, then distant.
3. Fib: prefer labeled ratios; if label unreadable, store price with `ratio: null`. Multiple pasted fib anchors → `fib_sets`.
4. VP shelves: load [luxalgo_vp_shelves.md](luxalgo_vp_shelves.md). Peaks = consolidation / acceptance; troughs / lowest volume = rejection / thin interest; highest volume = strong acceptance.
5. RSI: apply strength rules above whenever the pane is visible.
6. Structure notes may relate price to 50/100/200, fib/S/R/VP, channel, and RSI strength — **no news, no fundamentals**.
7. Do not invent levels not visible on the screenshot.

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
