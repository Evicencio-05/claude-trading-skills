# Prediction / process log v1.5

After each real `ta-confluence` session, append one row per charted ticker
(and optionally a session-level note). This is the Phase 1 learning seed
before Phase 2 behavioral tools.

**Path:** `reports/charts/confluence/prediction_log_YYYY-MM-DD.md` (+ optional `.json`)

**Accounts:** Only link Agentic (C) or taxable (A) outcomes — never IRA.

---

## When to write

1. After PHASE 4 persist of session / ticker confluence artifacts
2. Before or after `/agentic-copilot-trade` if a PLAY was taken
3. Next session: fill **outcome** columns for open rows (T+1 / T+5 as practical)

---

## Markdown table (append rows)

| as_of | ticker | mode | period | bias | tw_color | verdict | score | process_grade | confluence_path | taken? | account | outcome_T1 | outcome_T5 | notes |
|-------|--------|------|--------|------|----------|---------|-------|---------------|-----------------|--------|---------|------------|------------|-------|
| YYYY-MM-DD | TICKER | candle_first\|map_first | daily\|weekly | long\|short\|either | COLOR | PLAY\|WATCH\|NO_TRADE | 0–100 | A–F or text | `reports/charts/confluence/...` | Y/N | C\|A\|— | | | |

**taken?** = operator placed or sized a trade from this brief (usually C via Agentic).

**outcome_T\*** = brief result vs thesis (e.g. `+1R`, `stop`, `still open`, `N/A`).

---

## JSON shape (optional companion)

```json
{
  "source": "ta_confluence_prediction_log",
  "as_of": "YYYY-MM-DD",
  "rows": [
    {
      "ticker": "UMAC",
      "mode": "candle_first",
      "period": "daily",
      "bias": "long",
      "tw_color": "BLUE",
      "verdict": "WATCH",
      "score": 72,
      "process_grade": "B",
      "confluence_path": "reports/charts/confluence/UMAC_confluence_YYYY-MM-DD.json",
      "taken": false,
      "account": null,
      "outcome_t1": null,
      "outcome_t5": null,
      "notes": ""
    }
  ]
}
```

---

## Process retro (short)

Once per week or after 3+ sessions, add a few bullets under the day's log:

- What the rubric got right / wrong
- HTF fight false positives
- Missing operator chart near-misses
- One rubric or judgment prompt tweak (PR if durable)

Do **not** auto-merge rubric changes without human review.
