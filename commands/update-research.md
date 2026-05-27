---
description: "Perform a targeted update on an existing research report for a ticker: diff vs previous, thesis validation, updated scorecard, revised levels, and action recommendation."
argument-hint: "<TICKER>"
---

Perform a targeted update on an existing research report for {TICKER}.

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

Re-run only the data-fetching portions of each phase. Do NOT regenerate
prose or analysis from scratch — we only want to identify what changed.
Specifically, fetch:

  a. Market context: market-breadth-analyzer score, exposure-coach posture,
     market-top-detector distribution count.
  b. Price & technicals: current price, key MAs, RSI, volume trends,
     support/resistance levels. Has the stock broken any key levels since
     the last report?
  c. Fundamentals: any new earnings release since last report? Updated
     estimates? Analyst rating changes?
  d. Ownership: any 13F updates or notable insider transactions since
     the last report date?
  e. News: run market-news-analyst for events since the last report date.
  f. Screening: re-run VCP, CANSLIM, or theme checks if they were
     included in the original report.

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
