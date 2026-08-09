---
description: "Ingest the operator's TradingView charts (S/R, fib extensions, LuxAlgo VP shelves, 50/100/200 SMA) into dated markdown+JSON artifacts."
argument-hint: "<TICKER>"
---

# /operator-charts {TICKER}

Ingest **user-supplied** personal chart images for `{TICKER}`. Four indicators: white S/R, fib extensions, LuxAlgo VP shelves, SMA 50/100/200.

**Co-pilot only.** No MCP orders. No cross-source merge. No news/FMP.

**Artifact paths:** key `operator_charts` → `reports/charts/operator/`.

---

## Invoke

```
/operator-charts HOOD
```

Paste chart screenshot(s) in the same message.

---

## PHASE 0 — INTAKE

1. Require `{TICKER}` (uppercase).
2. `as_of` from chart date or today America/New_York.
3. Accept screenshot(s). If none, stop and ask.
4. Load:
   - [input_contract.md](../.cursor/skills/operator-charts/references/input_contract.md)
   - [luxalgo_vp_shelves.md](../.cursor/skills/operator-charts/references/luxalgo_vp_shelves.md) if VP visible

---

## PHASE 1 — EXTRACT

Fill envelope; populate `extracted` per the input contract (all four indicator groups when visible).

```json
{
  "source": "operator",
  "ticker": "{TICKER}",
  "as_of": "YYYY-MM-DD",
  "inputs": [{"type": "image", "note": "..."}],
  "extracted": {},
  "confidence": "high|medium|low",
  "gaps": [],
  "next": null
}
```

---

## PHASE 2 — PERSIST

- `reports/charts/operator/{TICKER}_operator_{as_of}.json`
- `reports/charts/operator/{TICKER}_operator_{as_of}.md`

Markdown: last, SMAs, nearest S/R + fib, VP shelves summary. **No trade plan.**

---

## Non-goals

- Merging with `tradewhisperer-charts` or `gex-vex-maps`
- Auto-invoking `technical-analyst`
- Trade plans, sizing, MCP execution
