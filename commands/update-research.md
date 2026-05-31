---
description: "Perform a targeted update on an existing research report for a ticker: diff vs previous, thesis validation, updated scorecard, revised levels, and action recommendation."
argument-hint: "<TICKER>"
---

Perform a targeted update on an existing research report for {TICKER}.

> **Cost discipline:** Reuse same-day batch artifacts via preflight manifest before re-running screeners or market context skills. See [project-docs/reference/cost-discipline.md](../project-docs/reference/cost-discipline.md).

STEP 0 — REUSE CHECK (zero LLM cost)

Run before fetching fresh data:

```bash
uv run python3 scripts/research_preflight.py --ticker {TICKER}
```

Add `--force-refresh` only when the user explicitly requests a full batch re-run.

1. Read `reports/logs/research_preflight_{TICKER}_{YYYY-MM-DD}.json`.
2. For each artifact with `"action": "reuse"`, read the cited `path` — do **not** re-run that skill.
3. For each artifact with `"action": "run"`, execute using the manifest `run_hint` when present.
4. If `market_context` action is `run`, run `uv run python3 scripts/pre_market.py`, then re-run preflight.

STEP 1 — LOAD PREVIOUS REPORT

Find the most recent report for {TICKER} by globbing reports/research/{TICKER}_*.md,
sorting the results by date descending, and reading the first (newest) file.
If no match exists, say so and suggest running /deep-research {TICKER} first.
Parse the previous report to extract:
  - The date it was generated.
  - The scorecard ratings from last time.
  - The bull/bear/base case probabilities.
  - The trade plan levels (entry, stop, targets).
  - The thesis invalidation triggers.

STEP 2 — FETCH FRESH DATA

Collect only what changed. Do NOT regenerate prose or analysis from scratch —
we only want to identify deltas. Use STEP 0 manifest (reuse-first).

  a. Market context / screeners (reuse-first): breadth, uptrend, exposure-coach,
     market-top, vcp, canslim, theme — read manifest paths when action=reuse;
     run skills only when action=run.
  b. Price & technicals (always refresh): current price, key MAs, RSI, volume trends,
     support/resistance levels. Has the stock broken any key levels since
     the last report?
  c. Fundamentals (refresh if stale): new earnings since last report, updated
     estimates, analyst rating changes.
  d. Ownership (refresh if stale): 13F updates or notable insider transactions since
     the last report date.
  e. News (always refresh): market-news-analyst or WebSearch for events since the
     last report date.
  f. Screening (conditional + reuse-first): if VCP, CANSLIM, or theme appeared in
     the original report, reuse manifest when action=reuse; run only when action=run
     or applicability changed (e.g. Stage 2 status flipped).

STEP 3 — DIFF ANALYSIS

Compare the fresh data against the previous report. For each phase,
categorize changes as:

  🟢 IMPROVED   — Metric moved favorably.
  🔴 DETERIORATED — Metric moved unfavorably.
  ⚪ UNCHANGED  — No material change.
  🟡 NEW INFO   — Something not in the previous report (new earnings,
                   new news, new filing).

STEP 4 — THESIS VALIDATION

Check each thesis invalidation trigger from the previous report:
  - Has any trigger been hit? If so, flag it prominently.
  - Have any triggers come close (within 5-10% of being triggered)?
  - Are the bull/bear/base case probabilities still appropriate given
    the new data, or should they shift?

STEP 5 — UPDATED SCORECARD

Regenerate the scorecard with new ratings. Show the previous rating
alongside the new one with an arrow indicating direction.

STEP 6 — GENERATE THE UPDATE REPORT

Format as:

# {TICKER} — Research Update
**Updated:** {today's date}
**Previous Report:** {date of last report}
**Days Since Last Report:** {N}

## Status: {THESIS INTACT / THESIS WEAKENED / THESIS INVALIDATED / THESIS STRENGTHENED}

## What Changed

### 🔴 Deteriorations
{List each negative change with brief explanation}

### 🟢 Improvements
{List each positive change with brief explanation}

### 🟡 New Information
{List new developments not in previous report}

### ⚪ Unchanged
{Brief note on what held steady}

## Updated Scorecard
| Dimension         | Previous | Current | Change |
|-------------------|----------|---------|--------|
| Market Context    |          |         | →/↑/↓  |
| Fundamentals      |          |         | →/↑/↓  |
| Valuation         |          |         | →/↑/↓  |
| Earnings Momentum |          |         | →/↑/↓  |
| Technical Setup   |          |         | →/↑/↓  |
| Ownership & Flow  |          |         | →/↑/↓  |
| Risk Profile      |          |         | →/↑/↓  |
| **Composite**     |          |         | →/↑/↓  |

## Thesis Invalidation Check
| Trigger                          | Status          |
|----------------------------------|-----------------|
| {trigger from original report}   | ✅ Clear / ⚠️ Close / ❌ Hit |
| ...                              |                 |

## Updated Probabilities
| Scenario   | Previous | Current | Shift   |
|------------|----------|---------|---------|
| Bull Case  |          |         |         |
| Base Case  |          |         |         |
| Bear Case  |          |         |         |

## Revised Key Levels
| Level            | Previous | Current | Notes              |
|------------------|----------|---------|--------------------|
| Entry            |          |         |                    |
| Stop             |          |         |                    |
| Target 1         |          |         |                    |
| Target 2         |          |         |                    |
| Target 3         |          |         |                    |

## Action Recommendation
Based on the changes, recommend one of:
  - **HOLD** — Thesis intact, no action needed.
  - **ADD** — Thesis strengthened, consider adding to position.
  - **TRIM** — Thesis weakening, consider reducing exposure.
  - **EXIT** — Invalidation trigger hit or thesis broken.
  - **UPGRADE** — Was previously Hold/Avoid, now actionable.
  - **DOWNGRADE** — Was previously Buy, now Hold or Avoid.

Explain the reasoning in 2-3 sentences.

## Data Sources & Gaps
{List sources used and any data that couldn't be refreshed}
Include `reports/logs/research_preflight_{TICKER}_{YYYY-MM-DD}.json` and cite reused artifact paths (action=reuse) vs freshly run items (action=run).

---
*Research update for educational purposes only. Not financial advice.*

STEP 7 — SAVE

1. Archive the current report (the {TICKER}_{old-date}.md file found in STEP 1) to
   reports/archives/{TICKER}_{old-date}.md using the date from its "Generated" line.

2. Read the FULL previous report content. Regenerate a COMPLETE updated
   report (not just the diff) incorporating all changes, and write it to
   reports/research/{TICKER}_{YYYY-MM-DD}.md where the date is today's date.
   The updated full report should follow the same format as the original
   /deep-research output but with all data points refreshed.

3. Append a summary entry to reports/logs/{TICKER}_changelog.md:

   ## {today's date}
   - Status: {INTACT/WEAKENED/INVALIDATED/STRENGTHENED}
   - Composite: {old} → {new}
   - Action: {HOLD/ADD/TRIM/EXIT/UPGRADE/DOWNGRADE}
   - Key changes: {1-2 sentence summary}
   ---

4. Confirm all saves.
