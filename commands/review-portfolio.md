---
description: "Run a batch update across all tracked tickers in reports/research/, showing staleness and offering to refresh selected or all reports with a portfolio summary table."
---

Run a batch update across all tracked tickers.

1. Glob reports/research/{TICKER}_{YYYY-MM-DD}.md files to identify active tickers.
   Filenames follow the pattern {TICKER}_{YYYY-MM-DD}.md — extract the ticker as
   everything before the first underscore-date suffix, and the date from the suffix.
   If multiple dated files exist for the same ticker, use the most recent date only.

2. For each ticker found, print:
   - Ticker, last report date (from filename), days since last update.

3. Sort by staleness (oldest update first).

4. Ask which tickers to update, or offer to update all.

5. For each selected ticker, run the equivalent of /update-research {TICKER} (includes STEP 0 preflight via `scripts/research_preflight.py` before fetching data).

6. After all updates complete, generate a portfolio summary table:

   # Portfolio Research Summary — {today's date}

   | Ticker | Last Updated | Composite | Trend  | Action       | Key Change       |
   |--------|-------------|-----------|--------|--------------|------------------|
   |        |             |           | ↑/→/↓  |              |                  |

   ## Alerts
   {List any tickers where invalidation triggers were hit or nearly hit}

   ## Stalest Reports
   {List any tickers not updated in >14 days}

   Save this summary to reports/logs/portfolio_summary_{YYYY-MM-DD}.md
